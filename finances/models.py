import datetime
import json

from django.db import models
from django.db import transaction as db_transaction
from django.contrib.auth.models import User

from homis_core.models import Person


class Transaction(models.Model):
    date = models.DateTimeField(default = datetime.datetime.now, blank = True)
    entered_by = models.ForeignKey(User)
    description = models.TextField(blank = True)
    #json = models.TextField()
    debt_graph_json = models.TextField(blank = True)

    @property
    def total(self):
        value = 0.0

        for item in self.items.all():
            value += float(item.paid_amount)

        return value

    @property
    def payers(self):
        return self.items.filter(paid_amount__gt = 0.0).all()

    @property
    def receivers(self):
        return self.items.filter(weight__gt = 0.0).all()

    def __unicode__(self):
        return u"{} on {}".format(self.total, self.date)

    def get_previous(self):
        transaction = (Transaction
            .objects
            .filter(date__lt = self.date)
            .order_by('-date').first())
        return transaction

    def get_debt_graph(self):
        json_string = self.debt_graph_json
        if json_string is None or json_string.strip() == "":
            return DebtGraph()
        return DebtGraph.from_json(json_string)

    def get_debts(self, person = None):
        debt_graph = self.get_debt_graph()

        if person is None:
            return debt_graph.debts

        result = []
        for debtor, creditor, debt in debt_graph.debts:
            if debtor.id == person.id:
                result.append((debtor, creditor, debt))

        return result

    def recalculate_debt_graph(self):
        previous = self.get_previous()

        debt_graph = None
        if previous is None:
            debt_graph = DebtGraph()
        else:
            debt_graph = previous.get_debt_graph()

        debt_graph.add_transaction(self)
        debt_graph.simplify()

        self.debt_graph_json = debt_graph.to_json()

    @classmethod
    def get_last(cls):
        try:
            return cls.objects.order_by("-date")[0]
        except IndexError:
            return None

    @classmethod
    def create_simple_payment(self, from_person, to_person, amount, current_user, description = ""):
        with db_transaction.atomic():
            transaction = Transaction(entered_by = current_user, description = description)
            transaction.save()

            item1 = TransactionItem(
                transaction = transaction,
                person = from_person,
                paid_amount = float(amount),
                weight = 0.0)

            item2 = TransactionItem(
                transaction = transaction,
                person = to_person)

            item1.save()
            item2.save()

            transaction.recalculate_debt_graph()
            transaction.save()

    @classmethod
    def create_complex(self, items, current_user, description = ""):
        with db_transaction.atomic():
            transaction = Transaction(
                entered_by = current_user,
                description = description)
            transaction.save()

            for person, amount, weight in items:
                item = TransactionItem(
                    transaction = transaction,
                    person = person,
                    paid_amount = amount,
                    weight = weight)
                item.save()

            transaction.recalculate_debt_graph()
            transaction.save()


class TransactionItem(models.Model):
    transaction = models.ForeignKey("Transaction", related_name="items")
    person      = models.ForeignKey(Person)
    paid_amount = models.FloatField(default = 0)
    weight      = models.FloatField(default = 1)

    def __unicode__(self):
        return u"{} paid {} received {}".format(
            self.person.nick_name,
            self.paid_amount,
            self.weight,
        )


class DebtEdge(object):
    def __init__(self, a, b):
        self.node_a = a
        self.node_b = b
        self.a_to_b = 0.0
        self.b_to_a = 0.0

    def normalize(self):
        min_value = min(self.a_to_b, self.b_to_a)
        if min_value < 0:
            self.a_to_b += abs(min_value)
            self.b_to_a += abs(min_value)
        elif min_value > 0:
            self.a_to_b -= min_value
            self.b_to_a -= min_value

    def get_opposite(self, node):
        if node is self.node_a:
            return self.node_b
        else:
            return self.node_a

    def get_debt(self, debtor):
        if debtor is self.node_a:
            return self.a_to_b
        else:
            return self.b_to_a

    def add_debt(self, debtor, amount):
        if debtor is self.node_a:
            print "%s IS %s" % (debtor, self.node_a)
            self.a_to_b += amount
        else:
            print "%s IS NOT %s" % (debtor, self.node_a)
            self.b_to_a += amount
        self.normalize()


class DebtNode(object):
    def __init__(self, person):
        self.person = person
        self.edges = {}

    def _get_edge(self, creditor_node, create = False):
        edge = None

        try:
            edge = self.edges[creditor_node]
        except KeyError:
            if create:
                edge = DebtEdge(self, creditor_node)
                self.edges[creditor_node] = edge
                creditor_node.edges[self] = edge

        return edge

    def add_debt(self, creditor_node, amount):
        edge = self._get_edge(creditor_node, True)
        edge.add_debt(self, amount)


class DebtGraph(object):
    def __init__(self):
        self.nodes = {}

    def _get_node(self, person):
        try:
            return self.nodes[person.id]
        except KeyError:
            node = DebtNode(person)
            self.nodes[person.id] = node
            return node

    def add_debt(self, debtor, creditor, amount):
        debtor_node = self._get_node(debtor)
        creditor_node = self._get_node(creditor)
        debtor_node.add_debt(creditor_node, amount)

    def add_transaction(self, t):
        items = t.items.all()
        payers = t.payers
        receivers = t.receivers

        total_weight = 0.0

        for item in items:
            total_weight += float(item.weight)

        for payer in payers:
            for receiver in receivers:
                if payer.person.id == receiver.person.id:
                    continue
                share = float(payer.paid_amount) * (float(receiver.weight) / total_weight)
                print "ADD %s -> %s : %f" % (receiver.person, payer.person, share)
                self.add_debt(receiver.person, payer.person, share)

    def simplify(self):
        change = True

        while change:
            change = False

            for debtor in self.nodes.values():
                for creditor1, edge1 in debtor.edges.items():
                    debt1 = edge1.get_debt(debtor)
                    if debt1 == 0:
                        continue
                    for creditor2, edge2 in creditor1.edges.items():
                        debt2 = edge2.get_debt(creditor1)
                        if debt2 == 0:
                            continue

                        min_amount = min(debt1, debt2)
                        edge1.add_debt(debtor, -min_amount)
                        edge2.add_debt(creditor1, -min_amount)

                        debtor.add_debt(creditor2, min_amount)

                        change = True

    @property
    def debts(self):
        for debtor in self.nodes.values():
            for creditor, edge in debtor.edges.items():
                debt = edge.get_debt(debtor)
                if debt > 0:
                    yield debtor.person, creditor.person, debt

    def to_json(self):
        value = []

        for debtor in self.nodes.values():
            for creditor, edge in debtor.edges.items():
                debt = edge.get_debt(debtor)
                if debt > 0:
                    print debtor.person, creditor.person, debt
                    value.append((debtor.person.id, creditor.person.id, debt))

        return json.dumps(value)

    @classmethod
    def from_json(self, json_string):
        value = json.loads(json_string)
        result = DebtGraph()

        for debtor_id, creditor_id, amount in value:
            debtor = Person.objects.get(pk = debtor_id)
            creditor = Person.objects.get(pk = creditor_id)
            result.add_debt(debtor, creditor, amount)

        return result


