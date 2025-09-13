import { useEffect, useState, useRef, useCallback } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  BarElement,
} from "chart.js";
import { Chart } from "react-chartjs-2";
import api from "../services/api";
import "./MarketChart.css";

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  BarElement
);

function MarketChart({ symbol, initialTimeframe = "1D" }) {
  const [timeframe, setTimeframe] = useState(initialTimeframe);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [indicators, setIndicators] = useState({
    sma: false,
    ema: false,
    rsi: false,
    volume: true,
  });
  const chartRef = useRef();

  // Timeframe options
  const timeframeOptions = [
    { value: "1D", label: "1 Day" },
    { value: "1W", label: "1 Week" },
    { value: "1M", label: "1 Month" },
    { value: "3M", label: "3 Months" },
    { value: "1Y", label: "1 Year" },
  ];

  // Simple Moving Average (SMA)
  const calculateSMA = useCallback((data, period = 20) => {
    const result = [];
    for (let i = 0; i < data.length; i++) {
      if (i < period - 1) {
        result.push(null);
      } else {
        let sum = 0;
        for (let j = 0; j < period; j++) {
          sum += data[i - j].close;
        }
        result.push(sum / period);
      }
    }
    return result;
  }, []);

  // Process chart data
  const processChartData = useCallback(
    (rawData) => {
      if (!rawData || rawData.length === 0) return;

      const labels = rawData.map((d) => {
        const date = new Date(d.datetime);
        return timeframe === "1D"
          ? date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
          : date.toLocaleDateString("en-US");
      });

      const closes = rawData.map((d) => parseFloat(d.close));
      const volumes = rawData.map((d) => parseFloat(d.volume) || 0);

      const datasets = [
        {
          type: "line",
          label: "Closing Price",
          data: closes,
          borderColor: "rgb(75, 192, 192)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderWidth: 2,
          fill: false,
          tension: 0.1,
          yAxisID: "y",
        },
      ];

      if (indicators.sma) {
        const smaData = calculateSMA(rawData, 20);
        datasets.push({
          type: "line",
          label: "SMA (20)",
          data: smaData,
          borderColor: "rgb(255, 99, 132)",
          borderWidth: 1.5,
          borderDash: [5, 5],
          pointStyle: false,
          fill: false,
          yAxisID: "y",
        });
      }

      if (indicators.volume) {
        datasets.push({
          type: "bar",
          label: "Volume",
          data: volumes,
          backgroundColor: "rgba(153, 102, 255, 0.2)",
          borderColor: "rgba(153, 102, 255, 1)",
          borderWidth: 1,
          yAxisID: "y1",
        });
      }

      setChartData({
        labels,
        datasets,
      });
    },
    [timeframe, indicators, calculateSMA]
  );

  // Fetch data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/market-data/${symbol}`, {
          params: { timeframe },
        });

        if (response.data && response.data.values) {
          processChartData(response.data.values);
          setError(null);
        } else {
          throw new Error("Invalid data format");
        }
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Failed to load market data. Try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [symbol, timeframe, processChartData]);

  // Chart options
  const options = {
    responsive: true,
    interaction: {
      mode: "index",
      intersect: false,
    },
    plugins: {
      legend: {
        position: "top",
        labels: {
          color: "#e5e7eb",
          usePointStyle: true,
        },
      },
      title: {
        display: true,
        text: `${symbol} - Closing Price`,
        color: "#e5e7eb",
        font: { size: 16 },
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            let label = context.dataset.label || "";
            if (label) {
              label += ": ";
            }
            if (context.parsed.y !== null) {
              if (context.dataset.label === "Volume") {
                label += new Intl.NumberFormat("en-US").format(
                  context.parsed.y
                );
              } else {
                label += new Intl.NumberFormat("en-US", {
                  style: "currency",
                  currency: "USD",
                }).format(context.parsed.y);
              }
            }
            return label;
          },
        },
      },
    },
    scales: {
      x: {
        grid: { color: "rgba(255, 255, 255, 0.1)" },
        ticks: { color: "#e5e7eb", maxTicksLimit: 10 },
      },
      y: {
        type: "linear",
        display: true,
        position: "left",
        grid: { color: "rgba(255, 255, 255, 0.1)" },
        ticks: {
          color: "#e5e7eb",
          callback: (value) => "$" + value.toFixed(2),
        },
      },
      y1: {
        type: "linear",
        display: indicators.volume,
        position: "right",
        grid: { drawOnChartArea: false },
        ticks: {
          color: "#e5e7eb",
          callback: (value) => {
            if (value >= 1000000) return (value / 1000000).toFixed(1) + "M";
            if (value >= 1000) return (value / 1000).toFixed(1) + "K";
            return value;
          },
        },
      },
    },
    maintainAspectRatio: false,
  };

  // Toggle indicators
  const toggleIndicator = (indicator) => {
    setIndicators((prev) => ({
      ...prev,
      [indicator]: !prev[indicator],
    }));
  };

  if (loading) {
    return (
      <div className="market-chart-container">
        <div className="chart-loading">Loading {symbol} data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="market-chart-container">
        <div className="chart-error">{error}</div>
        <button
          onClick={() => window.location.reload()}
          className="retry-button"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="market-chart-container">
      <div className="chart-header">
        <h2>{symbol} Chart</h2>
        <div className="chart-controls">
          <select
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="timeframe-selector"
          >
            {timeframeOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>

          <div className="indicator-toggles">
            <button
              className={indicators.sma ? "active" : ""}
              onClick={() => toggleIndicator("sma")}
            >
              SMA 20
            </button>
            <button
              className={indicators.volume ? "active" : ""}
              onClick={() => toggleIndicator("volume")}
            >
              Volume
            </button>
          </div>
        </div>
      </div>

      <div className="chart-wrapper">
        {chartData ? (
          <Chart ref={chartRef} type="line" data={chartData} options={options} />
        ) : (
          <div className="no-data">No data available</div>
        )}
      </div>

      <div className="chart-footer">
        <div className="price-info">
          Last price:{" "}
          {chartData && chartData.datasets[0].data.length > 0
            ? new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD",
              }).format(
                chartData.datasets[0].data[
                  chartData.datasets[0].data.length - 1
                ]
              )
            : "N/A"}
        </div>
        <div className="chart-legend">
          {indicators.sma && <span className="legend-sma">• SMA 20</span>}
          {indicators.volume && <span className="legend-volume">• Volume</span>}
        </div>
      </div>
    </div>
  );
}

export default MarketChart;
