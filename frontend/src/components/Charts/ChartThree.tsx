import { ApexOptions } from "apexcharts";
import React, { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import axios from "axios";
import { fetchWithAuth } from "@/utils/fetchWithAuth";

interface ChartThreeState {
  series: number[];
  labels: string[];
}

const options: ApexOptions = {
  chart: {
    fontFamily: "Satoshi, sans-serif",
    type: "donut",
  },
  colors: ["#3C50E0", "#6577F3", "#8FD0EF", "#0FADCF"],
  legend: {
    show: false,
    position: "bottom",
  },
  plotOptions: {
    pie: {
      donut: {
        size: "65%",
        background: "transparent",
      },
    },
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
    labels: [],
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchWithAuth(
          "http://127.0.0.1:5000/api/flights?per_page=1000",
        );
        const flightsData = await response.json();
        const flights = flightsData.flights;

        const aircraftTypeCounts: { [key: string]: number } = {};

        flights.forEach((flight: any) => {
          const type = flight.aircraft_type;
          if (!aircraftTypeCounts[type]) {
            aircraftTypeCounts[type] = 0;
          }
          aircraftTypeCounts[type]++;
        });

        const labels = Object.keys(aircraftTypeCounts);
        const data = Object.values(aircraftTypeCounts);

        setState({
          series: data,
          labels: labels,
        });
      } catch (error) {
        console.error("Error fetching flight data", error);
      }
    };

    fetchData();
  }, []);

  const updatedOptions = {
    ...options,
    labels: state.labels,
  };

  return (
    <div className="col-span-12 rounded-sm border border-stroke bg-white px-5 pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-5">
      <div className="mb-3 justify-between gap-4 sm:flex">
        <div>
          <h5 className="pb-4 text-xl font-semibold text-black dark:text-white">
            Flight Aircraft Types
          </h5>
        </div>
      </div>

      <div className="mb-2">
        <div id="chartThree" className="mx-auto flex justify-center">
          <ReactApexChart
            options={updatedOptions}
            series={state.series}
            type="donut"
          />
        </div>
      </div>

      <div className="-mx-8 flex flex-wrap items-center justify-center gap-y-3">
        {state.labels.map((label, index) => (
          <div key={label} className="w-full px-8 sm:w-1/2">
            <div className="flex w-full items-center">
              <span
                className={`mr-2 block h-3 w-full max-w-3 rounded-full`}
                style={{
                  backgroundColor: options.colors
                    ? options.colors[index]
                    : "defaultColor",
                }}
              ></span>
              <p className="flex w-full justify-between text-sm font-medium text-black dark:text-white">
                <span> {label} </span>
                <span>
                  {" "}
                  {(
                    (state.series[index] /
                      state.series.reduce((a, b) => a + b, 0)) *
                    100
                  ).toFixed(2)}
                  %{" "}
                </span>
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChartThree;
