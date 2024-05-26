"use client";
import { ApexOptions } from "apexcharts";
import React, { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";
import axios from "axios";
import Select from "react-select";
import countriesAndCities from "../CountryData/CountryData";

interface ChartThreeState {
  series: number[];
  days: string[];
}

interface CountryCities {
  [country: string]: string[];
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
          width: 600,
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

const WindChart: React.FC = () => {
  const [state, setState] = useState<ChartThreeState>({
    series: [],
    days: [],
  });
  const [selectedCountry, setSelectedCountry] = useState<string>(
    Object.keys(countriesAndCities)[0],
  );
  const [selectedCity, setSelectedCity] = useState<string>(
    countriesAndCities[selectedCountry][0],
  );

  useEffect(() => {
    fetchWeatherData(selectedCity);
  }, [selectedCity]);

  const fetchWeatherData = async (city: string) => {
    try {
      const response = await axios.get(
        `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${city}?include=fcst%2Cobs%2Chistfcst%2Cstats%2Cdays%2Chours%2Ccurrent%2Calerts&key=XMJF54BDVDFY3YXBQ84UE6P6A&options=beta&contentType=json`,
      );
      const forecast = response.data.days;
      const windSpeedData = forecast
        .map((day: any) => day.windspeed)
        .slice(0, 14); // Extract wind speed
      const days = forecast
        .map((day: any) => {
          const date = new Date(day.datetime);
          return `${date.toLocaleString("en", { month: "short" })} ${date.getDate()}`;
        })
        .slice(0, 14);
      setState({ series: windSpeedData, days });
    } catch (error) {
      console.error("Error fetching weather data:", error);
    }
  };

  const handleCountryChange = (selectedOption: any) => {
    const newCountry = selectedOption.value;
    setSelectedCountry(newCountry);
    setSelectedCity(countriesAndCities[newCountry][0]);
  };

  const handleCityChange = (selectedOption: any) => {
    setSelectedCity(selectedOption.value);
  };

  const countryOptions = Object.keys(countriesAndCities)
    .sort()
    .map((country) => ({
      value: country,
      label: country,
    }));

  const cityOptions = countriesAndCities[selectedCountry]
    .sort()
    .map((city) => ({
      value: city,
      label: city,
    }));

  return (
    <div className="col-span-12 w-full rounded-sm border border-stroke bg-white px-5 pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-5">
      <div className="mb-3 justify-between sm:flex">
        <div className="flex items-center">
          <h5 className="text-xl font-semibold text-black dark:text-white">
            Wind Speed
          </h5>
        </div>
        <div className="flex w-2/4">
          <Select
            className="z-9999 mb-2 mr-2 w-1/2 text-black"
            value={{ value: selectedCountry, label: selectedCountry }}
            onChange={handleCountryChange}
            options={countryOptions}
          />
          <Select
            className="z-9999 mb-2 w-1/2 text-black"
            value={{ value: selectedCity, label: selectedCity }}
            onChange={handleCityChange}
            options={cityOptions}
          />
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
            series={[{ name: "Wind Speed", data: state.series }]} // Updated series name to Wind Speed
            type="line"
          />
        </div>
      </div>

      <div className="-mx-8 flex flex-wrap items-center justify-center gap-y-3">
        {state.series.map(
          (
            windSpeed,
            index, // Updated variable name to windSpeed
          ) => (
            <div className="w-full px-8 sm:w-1/2" key={index}>
              <div className="flex w-full items-center">
                <p className="flex w-full justify-between text-sm font-medium text-black dark:text-white">
                  <span style={{ width: "60px" }}>{state.days[index]}</span>
                  <span>{windSpeed} m/s</span>{" "}
                  {/* Adjusted for wind speed in meters per second */}
                </p>
              </div>
            </div>
          ),
        )}
      </div>
    </div>
  );
};

export default WindChart;
