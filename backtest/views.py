from rest_framework.views import APIView
from rest_framework.response import Response
from market.services import FinancialDataService
from .services import run_backtest

class BacktestView(APIView):
    def post(self, request):
        symbol = request.data.get("symbol", "").upper()
        period = request.data.get("period", "3mo")
        interval = request.data.get("interval", "1h")
        initial = float(request.data.get("initial_capital", 10000))
        risk_pct = float(request.data.get("risk_pct", 1.0))
        sl_pct = float(request.data.get("stop_loss_pct", 2.0))

        df = FinancialDataService.fetch_history(symbol, period=period, interval=interval)
        if df.empty:
            return Response({"error": "No historical data"}, status=400)

        result = run_backtest(df, initial_capital=initial,
                              risk_pct=risk_pct, stop_loss_pct=sl_pct)
        return Response(result)