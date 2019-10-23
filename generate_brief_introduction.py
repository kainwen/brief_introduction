from jinja2 import Template
from trello import TrelloClient

import os


class NotFoundError(Exception):
    pass


class BriefIntro:

    def __init__(self):
        self.client = TrelloClient(api_key=os.getenv('TRELLO_API_KEY'),
                                   api_secret=os.getenv('TRELLO_API_SECRET'),
                                   token=os.getenv('OAUTH_TOKEN'),
                                   token_secret=os.getenv('OAUTH_TOKEN_SECRET'))

    def get_board_by_name(self, name):
        r = [b for b in self.client.list_boards() if b.name == name]
        if r:
            return r[0]
        else:
            raise NotFoundError

    def get_list_by_name(self, board, name):
        r = [l for l in board.all_lists() if l.name == name]
        if r:
            return r[0]
        else:
            raise NotFoundError

    def build_comments(self, comments):
        return [
            {'name': c['memberCreator']['fullName'],
             'text': c['data']['text']}
            for c in comments
        ]

    def build_cards(self, lst):
        return [self.build_card(card) for card in lst.list_cards()]

    def build_card(self, card):
        return {
            'title': card.name,
            'label': card.labels[0].name,
            'abstract': card.description,
            'comments': self.build_comments(card.comments)
        }

    def code_gen(self, board_name, list_name, title, outfile):
        b = self.get_board_by_name(board_name)
        l = self.get_list_by_name(b, list_name)
        cards = self.build_cards(l)
        with open("templates/brief_intro.md") as f:
            tpl = Template(f.read())
        with open(outfile, "w") as g:
            print(tpl.render(cards=cards, title=title), file=g)

    def get_vote(self, board_name, list_name, topk=5):
        b = self.get_board_by_name(board_name)
        l = self.get_list_by_name(b, list_name)
        cards = l.list_cards()
        votes = [(c, len(c.member_ids)) for c in cards]
        votes.sort(key=lambda p: p[1], reverse=True)
        for c, v in votes[:topk]:
            print(v, c.name)


if __name__ == "__main__":
    br = BriefIntro()
    br.get_vote("VLDB2019", "待办")
    #br.code_gen("VLDB2019", "待办", "VLDB2019简评", "/Users/zlv/Hack/trello/br.md")
