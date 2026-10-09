import random

try:
    from .base_game import Game
except ImportError:
    from base_game import Game

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


class Blackjack(Game):
    name = "Blackjack"

    def play(self) -> int:
        self._print_header(f"Welcome, {self.player_name}!")
        chips = 100

        while chips > 0:
            bet = self._get_bet(chips)
            if bet is None:
                break
            result = self._play_round()
            chips += bet if result == "win" else (-bet if result == "lose" else 0)
            self.score = max(self.score, chips)
            print(f"  💰 Chips: {chips}")

        print(f"\nFinal chips: {chips}")
        return self.score

    def _get_bet(self, chips: int):
        while True:
            raw = self._prompt(f"Bet (1-{chips}, or 'q' to quit)")
            if raw.lower() == "q":
                return None
            if raw.isdigit() and 0 < int(raw) <= chips:
                return int(raw)
            print("  Invalid bet.")

    def _deal(self):
        return random.choice(RANKS), random.choice(SUITS)

    def _hand_value(self, hand):
        total, aces = 0, 0
        for rank, _ in hand:
            if rank in ("J", "Q", "K"):
                total += 10
            elif rank == "A":
                total += 11
                aces += 1
            else:
                total += int(rank)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def _show(self, hand, label, hide_first=False):
        if hide_first:
            cards = f"[??] {hand[1][0]}{hand[1][1]}"
        else:
            cards = " ".join(f"{r}{s}" for r, s in hand)
        print(f"  {label}: {cards} ({self._hand_value(hand)})")

    def _play_round(self):
        player = [self._deal(), self._deal()]
        dealer = [self._deal(), self._deal()]

        self._show(dealer, "Dealer", hide_first=True)
        self._show(player, "You   ")

        while self._hand_value(player) < 21:
            if self._prompt("Hit or stand? (h/s)").lower() != "h":
                break
            player.append(self._deal())
            self._show(player, "You   ")
            if self._hand_value(player) > 21:
                print("  💥 Bust!")
                return "lose"

        self._show(dealer, "Dealer")
        while self._hand_value(dealer) < 17:
            dealer.append(self._deal())
            self._show(dealer, "Dealer")

        p, d = self._hand_value(player), self._hand_value(dealer)
        if d > 21 or p > d:
            print("  🎉 You win!")
            return "win"
        if p == d:
            print("  🤝 Push.")
            return "push"
        print("  😢 Dealer wins.")
        return "lose"