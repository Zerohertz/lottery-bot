import zerohertzLib as zz


class Notification(zz.api.SlackBot):
    def send_lotto_buying_message(self, body: dict) -> None:
        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":
            return
        lotto_number_str = self.make_lotto_number_message(result["arrGameChoiceNum"])
        message = f"{result['buyRound']}회 로또 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{lotto_number_str}```"
        self.message(message)

    def make_lotto_number_message(self, lotto_number: list) -> str:
        assert type(lotto_number) == list
        lotto_number = [x[:-1] for x in lotto_number]
        lotto_number = [x.replace("|", " ") for x in lotto_number]
        lotto_number = "\n".join(x for x in lotto_number)
        return lotto_number

    def send_win720_buying_message(self, body: dict) -> None:
        if body.get("resultCode") != "100":
            return
        win720_round = body.get("resultMsg").split("|")[3]
        win720_number_str = self.make_win720_number_message(body.get("saleTicket"))
        message = f"{win720_round}회 연금복권 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{win720_number_str}```"
        self.message(message)

    def make_win720_number_message(self, win720_number: str) -> str:
        return "\n".join(win720_number.split(","))

    def send_lotto_winning_message(self, winning: dict) -> None:
        assert type(winning) == dict
        try:
            message = f"로또 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 :tada:"
            self.message(message)
        except KeyError:
            message = "로또 6/45 - 낙첨입니다... :sob:"
            self.message(message)
            return

    def send_win720_winning_message(self, winning: dict) -> None:
        assert type(winning) == dict
        try:
            message = (
                f"연금복권 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 :tada:"
            )
            self.message(message)
        except KeyError:
            return
