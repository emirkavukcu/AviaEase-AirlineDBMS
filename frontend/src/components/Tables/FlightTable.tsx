"use client";

import React, { useState, useEffect } from "react";
import Select from "react-select";
import VirtualizedSelect from "./VirtualizedSelect";
import Link from "next/link";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import countries from "i18n-iso-countries";
import { fetchWithAuth } from "@/utils/fetchWithAuth";

countries.registerLocale(require("i18n-iso-countries/langs/en.json"));

interface Flight {
  airline_code: string;
  date_time: string;
  destination_airport: string;
  distance: number;
  duration: number;
  flight_number: number;
  source_airport: string;
  status: string;
  aircraft_type: string;
}

const FlightTable = () => {
  const [flights, setFlights] = useState<Flight[]>([]);
  const [filterApplied, setFilterApplied] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalCount, setTotalCount] = useState<number>(0);

  const [airports, setAirports] = useState<any[]>([]);

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [minDistance, setMinDistance] = useState<number | null>(null);
  const [maxDistance, setMaxDistance] = useState<number | null>(null);

  const [flightNumber, setFlightNumber] = useState<number | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [vehicleTypeId, setVehicleTypeId] = useState<number | null>(null);

  const [selectedCountrySource, setSelectedCountrySource] = useState<any>(null);
  const [selectedCitySource, setSelectedCitySource] = useState<any>(null);
  const [selectedAirportSource, setSelectedAirportSource] = useState<any>(null);

  const [selectedCountryDestination, setSelectedCountryDestination] =
    useState<any>(null);
  const [selectedCityDestination, setSelectedCityDestination] =
    useState<any>(null);
  const [selectedAirportDestination, setSelectedAirportDestination] =
    useState<any>(null);

  const [airportOptionsSource, setAirportOptionsSource] = useState<any[]>([]);
  const [citiesSource, setCitiesSource] = useState<any[]>([]);

  const [citiesDestination, setCitiesDestination] = useState<any[]>([]);
  const [airportOptionsDestination, setAirportOptionsDestination] = useState<
    any[]
  >([]);

  useEffect(() => {
    const fetchAirports = async () => {
      try {
        const response = await fetchWithAuth(
          "http://127.0.0.1:5000/api/airports",
        );
        const data = await response.json();
        setAirports(data);
      } catch (error) {
        console.error("Failed to fetch airports", error);
      }
    };

    fetchAirports();
  }, []);

  useEffect(() => {
    if (selectedCountrySource) {
      const countryCities = airports
        .filter((airport) => airport.country === selectedCountrySource)
        .map((airport) => airport.city)
        .sort();
      setCitiesSource([...new Set(countryCities)]);
    }
  }, [selectedCountrySource]);

  useEffect(() => {
    if (selectedCitySource) {
      const cityAirports = airports
        .filter((airport) => airport.city === selectedCitySource)
        .map((airport) => airport.airport_code);
      setAirportOptionsSource(cityAirports);
    }
  }, [selectedCitySource]);

  useEffect(() => {
    if (selectedCountryDestination) {
      const countryCities = airports
        .filter((airport) => airport.country === selectedCountryDestination)
        .map((airport) => airport.city)
        .sort();
      setCitiesDestination([...new Set(countryCities)]);
    }
  }, [selectedCountryDestination]);

  useEffect(() => {
    if (selectedCityDestination) {
      const cityAirports = airports
        .filter((airport) => airport.city === selectedCityDestination)
        .map((airport) => airport.airport_code);
      setAirportOptionsDestination(cityAirports);
    }
  }, [selectedCityDestination]);

  const fetchFlights = async () => {
    try {
      let url = new URL("http://127.0.0.1:5000/api/flights");
      let params = new URLSearchParams();

      if (startDate) params.append("min_date_time", startDate);
      if (endDate) params.append("max_date_time", endDate);
      if (minDistance) params.append("min_distance", minDistance.toString());
      if (maxDistance) params.append("max_distance", maxDistance.toString());
      if (flightNumber) params.append("flight_number", flightNumber.toString());
      if (status) params.append("status", status);
      if (vehicleTypeId)
        params.append("aircraft_type_id", vehicleTypeId.toString());

      if (selectedCountrySource) {
        const isoCode = countries.getAlpha2Code(selectedCountrySource, "en");
        if (isoCode) params.append("source_country", isoCode);
      }
      if (selectedCitySource) params.append("source_city", selectedCitySource);
      if (selectedAirportSource)
        params.append("source_airport", selectedAirportSource);

      if (selectedCountryDestination) {
        const isoCode = countries.getAlpha2Code(
          selectedCountryDestination,
          "en",
        );
        if (isoCode) params.append("destination_country", isoCode);
      }
      if (selectedCityDestination)
        params.append("destination_city", selectedCityDestination);
      if (selectedAirportDestination)
        params.append("destination_airport", selectedAirportDestination);
      params.append("page", currentPage.toString());

      url.search = params.toString();

      const response = await fetchWithAuth(url.toString());
      const data = await response.json();
      setFlights(data.flights);
      setTotalPages(data.pages);
      setTotalCount(data.total);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    fetchFlights();
  }, [filterApplied, currentPage]);

  const handleFilterApply = () => {
    setCurrentPage(1); // Reset to the first page
    setFilterApplied((prevValue) => prevValue + 1);
  };

  const handlePageChange = (
    event: React.ChangeEvent<unknown>,
    value: number,
  ) => {
    setCurrentPage(value);
  };

  const uniqueCountryOptions = Array.from(
    new Set(airports.map((airport) => airport.country)),
  )
    .sort()
    .map((country) => ({ value: country, label: country }));

  const statusOptions = [
    { value: "passed", label: "Passed" },
    { value: "active", label: "Active" },
    { value: "pending", label: "Pending" },
  ];

  const aircraftOptions = [
    { value: 1, label: "Boeing 737" },
    { value: 2, label: "Airbus A320" },
    { value: 3, label: "Boeing 777" },
  ];

  return (
    <div className="flex">
      <aside className="flex w-64 flex-col gap-y-2 bg-slate-50 p-4 pt-10 text-black dark:border-strokedark dark:bg-boxdark dark:text-white">
        <h1 className="pb-4 text-2xl font-bold">Filters</h1>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Flight Number</label>
          <input
            type="number"
            placeholder="Flight Number"
            value={flightNumber || ""}
            className="w-full rounded border p-2"
            onChange={(e) =>
              setFlightNumber(e.target.value ? Number(e.target.value) : null)
            }
          />
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-4 pb-4">
          <h3 className="text-xl font-semibold">Dates</h3>
          <div className="pb-2">
            <label htmlFor="startDate" className=" pr-1.5 font-medium">
              Start
            </label>
            <br />
            <input
              type="date"
              id="startDate"
              name="startDate"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div className="">
            <label htmlFor="endDate" className="pr-3 font-medium">
              End
            </label>
            <br />
            <input
              type="date"
              id="endDate"
              name="endDate"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <h3 className="pb-2 text-lg font-semibold">Source Airport</h3>
          <div className="mb-4.5">
            <label className="mb-3 block font-medium text-black dark:text-white">
              Country
            </label>
            <Select
              options={uniqueCountryOptions}
              placeholder="Select Country"
              onChange={(selectedOption) =>
                setSelectedCountrySource(selectedOption?.value)
              }
              value={uniqueCountryOptions.find(
                (country) => country.value === selectedCountrySource,
              )}
              isClearable
            />
          </div>
          <div className="mb-4.5">
            <label className="mb-3 block font-medium text-black dark:text-white">
              City
            </label>
            <Select
              options={citiesSource.map((city) => ({
                value: city,
                label: city,
              }))}
              placeholder="Select City"
              onChange={(selectedOption) =>
                setSelectedCitySource(selectedOption?.value)
              }
              isDisabled={!selectedCountrySource}
              value={
                selectedCitySource
                  ? { value: selectedCitySource, label: selectedCitySource }
                  : null
              }
              isClearable
            />
          </div>
          <div className="mb-4.5">
            <label className="tfont-medium mb-3 block text-black dark:text-white">
              Airport
            </label>
            <Select
              options={airportOptionsSource.map((airport) => ({
                value: airport,
                label: airport,
              }))}
              placeholder="Select Airport"
              onChange={(selectedOption) =>
                setSelectedAirportSource(selectedOption?.value)
              }
              isDisabled={!selectedCitySource}
              value={
                selectedAirportSource
                  ? {
                      value: selectedAirportSource,
                      label: selectedAirportSource,
                    }
                  : null
              }
              isClearable
            />
          </div>
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <h3 className="pb-2 text-lg font-semibold">Destination Airport</h3>
          <div className="mb-4.5">
            <label className="mb-3 block font-medium text-black dark:text-white">
              Country
            </label>
            <Select
              options={uniqueCountryOptions}
              placeholder="Select Country"
              onChange={(selectedOption) =>
                setSelectedCountryDestination(selectedOption?.value)
              }
              value={uniqueCountryOptions.find(
                (country) => country.value === selectedCountryDestination,
              )}
              isClearable
            />
          </div>
          <div className="mb-4.5">
            <label className="mb-3 block font-medium text-black dark:text-white">
              City
            </label>
            <Select
              options={citiesDestination.map((city) => ({
                value: city,
                label: city,
              }))}
              placeholder="Select City"
              onChange={(selectedOption) =>
                setSelectedCityDestination(selectedOption?.value)
              }
              isDisabled={!selectedCountryDestination}
              value={
                selectedCityDestination
                  ? {
                      value: selectedCityDestination,
                      label: selectedCityDestination,
                    }
                  : null
              }
              isClearable
            />
          </div>
          <div className="mb-4.5">
            <label className="tfont-medium mb-3 block text-black dark:text-white">
              Airport
            </label>
            <Select
              options={airportOptionsDestination.map((airport) => ({
                value: airport,
                label: airport,
              }))}
              placeholder="Select Airport"
              onChange={(selectedOption) =>
                setSelectedAirportDestination(selectedOption?.value)
              }
              isDisabled={!selectedCityDestination}
              value={
                selectedAirportDestination
                  ? {
                      value: selectedAirportDestination,
                      label: selectedAirportDestination,
                    }
                  : null
              }
              isClearable
            />
          </div>
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Distance</label>
          <div className="flex space-x-2">
            <input
              type="number"
              placeholder="min"
              value={minDistance || ""}
              className="w-22 rounded border p-2"
              onChange={(e) =>
                setMinDistance(e.target.value ? Number(e.target.value) : null)
              }
            />
            <span className=" mt-2">-</span>
            <input
              type="number"
              placeholder="max"
              value={maxDistance || ""}
              className="w-22 rounded border p-2"
              onChange={(e) =>
                setMaxDistance(e.target.value ? Number(e.target.value) : null)
              }
            />
          </div>
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Status</label>
          <Select
            options={statusOptions}
            placeholder="Select Status"
            onChange={(selectedOption) =>
              setStatus(selectedOption ? selectedOption.value : null)
            }
            isClearable
          />
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Aircraft</label>
          <Select
            options={aircraftOptions}
            placeholder="Select Aircraft"
            onChange={(selectedOption) =>
              setVehicleTypeId(selectedOption ? selectedOption.value : null)
            }
            isClearable
          />
        </div>

        <div className="flex justify-center">
          <div
            className=" inline-flex w-50 cursor-pointer items-center justify-center rounded-full bg-primary px-4 py-4 text-center text-lg font-medium text-white hover:bg-opacity-90"
            onClick={handleFilterApply}
          >
            Apply Filters
          </div>
        </div>
      </aside>

      <div className="rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
        <div className="mb-4 flex items-center justify-between ">
          <h4 className="text-2xl font-semibold text-black dark:text-white">
            Flights
          </h4>
          <h4 className="text-2xl font-semibold text-black dark:text-white">
            Total of {totalCount} Flights Found
          </h4>
          <Link
            href="/flights/create"
            className="items-center justify-center rounded-md bg-meta-3 px-8 py-4 text-center text-xl font-medium text-white hover:bg-opacity-90 lg:px-6 xl:px-6"
          >
            Create Flight
          </Link>
        </div>
        <div className="flex flex-col">
          <div className="grid grid-cols-3 rounded-sm bg-gray-2 dark:bg-meta-4 sm:grid-cols-7">
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Flight No
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Date
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Distance
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Source
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Destination
              </h5>
            </div>
            <div className="hidden p-2.5 sm:block xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Aircraft
              </h5>
            </div>
            <div className="hidden p-2.5 sm:block xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Status
              </h5>
            </div>
          </div>

          {flights.map((flight, key) => (
            <Link href={`/flights/${flight.flight_number}`} key={key}>
              <div
                className={`grid cursor-pointer grid-cols-3 hover:bg-slate-200 dark:hover:bg-meta-4 sm:grid-cols-7 ${
                  key === flights.length - 1
                    ? ""
                    : "border-b border-stroke dark:border-strokedark"
                }`}
              >
                <div className="flex items-center justify-center p-2.5">
                  <p className="hidden text-black dark:text-white sm:block">
                    {flight.flight_number}
                  </p>
                </div>
                <div className="flex items-center justify-center p-2.5">
                  <p className="text-center text-black dark:text-white">
                    {(() => {
                      const date = new Date(flight.date_time);
                      const day = date.getDate().toString().padStart(2, "0");
                      const month = (date.getMonth() + 1)
                        .toString()
                        .padStart(2, "0"); // Months are 0-indexed in JavaScript
                      const year = date.getFullYear().toString().slice(2);
                      const hours = date.getHours().toString().padStart(2, "0");
                      const minutes = date
                        .getMinutes()
                        .toString()
                        .padStart(2, "0");
                      return [
                        `${day}/${month}/${year}`,
                        <br key="br" />,
                        `${hours}:${minutes}`,
                      ];
                    })()}
                  </p>
                </div>
                <div className="flex items-center justify-center p-2.5">
                  <p className="text-black dark:text-white">
                    {flight.distance}km
                  </p>
                </div>
                <div className="hidden items-center justify-center p-2.5 sm:flex">
                  <p className="text-black dark:text-white">
                    {flight.source_airport}
                  </p>
                </div>
                <div className="hidden items-center justify-center p-2.5 sm:flex">
                  <p className="text-black dark:text-white">
                    {flight.destination_airport}
                  </p>
                </div>
                <div className="hidden items-center justify-center p-2.5 sm:flex">
                  <p className="text-black dark:text-white">
                    {flight.aircraft_type}
                  </p>
                </div>
                <div className="hidden items-center justify-center p-2.5 sm:flex">
                  <p className="text-black dark:text-white">
                    {flight.status.charAt(0).toUpperCase() +
                      flight.status.slice(1)}
                  </p>
                </div>
              </div>
            </Link>
          ))}
          <Stack spacing={2} alignItems="center" className="mt-4">
            <Pagination
              count={totalPages}
              page={currentPage}
              onChange={handlePageChange}
              color="primary"
              size="large"
              variant="outlined"
              shape="rounded"
              siblingCount={1}
              showFirstButton
              showLastButton
            />
          </Stack>
        </div>
      </div>
    </div>
  );
};

export default FlightTable;
