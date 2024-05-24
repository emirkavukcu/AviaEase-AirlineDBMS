import { ApexOptions } from "apexcharts";
import React, { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";
import axios from "axios";

interface ChartThreeState {
  series: number[];
  days: string[];
}

const options: ApexOptions = {
  chart: {
    fontFamily: "Satoshi, sans-serif",
    type: "line",
  },
  colors: ["#3C50E0"],
  legend: {
    show: false,
    position: "bottom",
  },
  dataLabels: {
    enabled: false,
  },
  responsive: [
    {
      breakpoint: 2600,
      options: {
        chart: {
          width: 380,
        },
      },
    },
    {
      breakpoint: 640,
      options: {
        chart: {
          width: 200,
        },
      },
    },
  ],
};

const ChartThree: React.FC = () => {
  const [state, setState] = useState<ChartThreeState>({
    series: [],
    days: [],
  });

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const response = await axios.get(
          "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Istanbul?include=fcst%2Cobs%2Chistfcst%2Cstats%2Cdays%2Chours%2Ccurrent%2Calerts&key=XMJF54BDVDFY3YXBQ84UE6P6A&options=beta&contentType=json"
        );
        const forecast = response.data.days;
        const weatherData = forecast.map((day: any) => Math.round((day.tempmax - 32) * (5 / 9)));
        const days = forecast.map((day: any) => day.datetime.split("-")[2]);
        setState({ series: weatherData, days });
      } catch (error) {
        console.error("Error fetching weather data:", error);
      }
    };

    fetchWeatherData();
  }, []);

  return (
    <div className="col-span-12 rounded-sm border border-stroke bg-white px-5 pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-5">
      <div className="mb-3 justify-between gap-4 sm:flex">
        <div>
          <h5 className="text-xl font-semibold text-black dark:text-white">
            Weekly Weather Forecast for Istanbul
          </h5>
        </div>
      </div>

      <div className="mb-2">
        <div id="chartThree" className="mx-auto flex justify-center">
          <ReactApexChart
            options={{
              ...options,
              xaxis: {
                categories: state.days,
              },
            }}
            series={[{ name: "Temperature", data: state.series }]}
            type="line"
          />
        </div>
      </div>

      <div className="-mx-8 flex flex-wrap items-center justify-center gap-y-3">
        {state.series.map((temp, index) => (
          <div className="w-full px-8 sm:w-1/2" key={index}>
            <div className="flex w-full items-center">
              <p className="flex w-full justify-between text-sm font-medium text-black dark:text-white">
                <span style={{ width: "60px" }}>Day {state.days[index]}</span>
                <span>{temp}°C</span>
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChartThree;