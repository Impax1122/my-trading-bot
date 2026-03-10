from AlgorithmImports import *


class MyTradingBot(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)

        # NQ Continuous Futures Contract
        self.nq = self.AddFuture(
            Futures.Indices.NASDAQ100EMini,
            resolution=Resolution.Minute,
            extendedMarketHours=True,
        )
        self.nq.SetFilter(0, 90)  # contracts expiring within 0-90 days

        self.front_contract = None

    def OnData(self, data: Slice):
        # Track the front-month contract
        for chain in data.FutureChains.Values:
            contracts = sorted(chain, key=lambda c: c.Expiry)
            if contracts:
                self.front_contract = contracts[0].Symbol

        if self.front_contract is None:
            return

        if not self.Portfolio.Invested:
            self.MarketOrder(self.front_contract, 1)

    def OnOrderEvent(self, order_event: OrderEvent):
        if order_event.Status == OrderStatus.Filled:
            self.Debug(
                f"Order filled: {order_event.Symbol} "
                f"Qty={order_event.FillQuantity} "
                f"Price={order_event.FillPrice}"
            )
