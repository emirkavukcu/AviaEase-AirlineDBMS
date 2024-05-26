import { ApexOptions } from "apexcharts";
import React, { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";
import axios from "axios";
import countriesAndCities from "../CountryData/CountryData";
import Select, { SingleValue } from "react-select";

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

const WeatherChart: React.FC = () => {
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
      const weatherData = forecast
        .map((day: any) => Math.round((day.tempmax - 32) * (5 / 9)))
        .slice(0, 14); // Get the first 14 elements
      const days = forecast
        .map((day: any) => {
          const date = new Date(day.datetime);
          return `${date.toLocaleString("en", { month: "short" })} ${date.getDate()}`;
        })
        .slice(0, 14); // Get the first 14 elements
      setState({ series: weatherData, days });
    } catch (error) {
      console.error("Error fetching weather data:", error);
    }
  };

  const handleCountryChange = (
    selectedOption: SingleValue<{ value: string; label: string }>,
  ) => {
    const newCountry =
      selectedOption?.value || Object.keys(countriesAndCities)[0];
    setSelectedCountry(newCountry);
    setSelectedCity(countriesAndCities[newCountry][0]);
  };

  const handleCityChange = (
    selectedOption: SingleValue<{ value: string; label: string }>,
  ) => {
    const newCity =
      selectedOption?.value || countriesAndCities[selectedCountry][0];
    setSelectedCity(newCity);
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

  const customStyles = {
    container: (provided: any) => ({
      ...provided,
      width: 150,
    }),
    menu: (provided: any) => ({
      ...provided,
      zIndex: 9999, // Ensure the dropdown appears on top
    }),
  };

  return (
    <div className=" col-span-12 w-full rounded-sm border border-stroke bg-white p-20 px-5 pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-5">
      <div className="mb-3 justify-between gap-4 sm:flex">
        <div className="flex items-center">
          <h5 className="text-xl font-semibold text-black dark:text-white">
            Weather Forecast
          </h5>
        </div>
        <div className="flex">
          <Select
            className="z-9999 mb-2 mr-2 w-1/2 text-black"
            styles={customStyles}
            value={{ value: selectedCountry, label: selectedCountry }}
            onChange={handleCountryChange}
            options={countryOptions}
          />
          <Select
            className="z-9999 mb-2 mr-2 w-1/2 text-black"
            styles={customStyles}
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
                <span style={{ width: "60px" }}>{state.days[index]}</span>
                <span>{temp}°C</span>
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WeatherChart;
