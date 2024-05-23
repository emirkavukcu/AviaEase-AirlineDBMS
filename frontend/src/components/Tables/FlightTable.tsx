"use client";
import React, { useState, useEffect } from "react";
import Select from "react-select";
import VirtualizedSelect from "./VirtualizedSelect";
import Link from "next/link";

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
  const [flights, setFlights] = useState<Flight[]>([]); // This should be fetched or passed as props
  const [filterApplied, setFilterApplied] = useState<number>(0);
  useEffect(() => {
    const fetchFlights = async () => {
      try {
        let url = new URL("http://127.0.0.1:5000/api/flights");
        let params = new URLSearchParams();

        if (startDate) params.append("min_date_time", startDate);
        if (endDate) params.append("max_date_time", endDate);
        if (minDistance) params.append("min_distance", minDistance.toString());
        if (maxDistance) params.append("max_distance", maxDistance.toString());
        if (sourceAirport) params.append("source_airport", sourceAirport.value);
        if (destinationAirport)
          params.append("destination_airport", destinationAirport.value);

        url.search = params.toString();

        const response = await fetch(url.toString());
        const data = await response.json();
        setFlights(data.flights);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchFlights();
  }, [filterApplied]);

  const [airports, setAirports] = useState<any>([]);
  useEffect(() => {
    const fetchAirports = async () => {
      try {
        let url = "http://127.0.0.1:5000/api/airport_codes";
        const response = await fetch(url);
        const data = await response.json();
        setAirports(data);
        console.log(data);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchAirports();
  }, []);

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [minDistance, setMinDistance] = useState<number | null>(null);
  const [maxDistance, setMaxDistance] = useState<number | null>(null);
  const [sourceAirport, setSourceAirport] = useState<any>("");
  const [destinationAirport, setDestinationAirport] = useState<any>("");

  const airportOptions = airports.map((airport: string) => ({
    value: airport,
    label: airport,
  }));

  return (
    <div className="flex">
      <aside className="flex w-64 flex-col gap-y-2 p-4 text-black">
        <h1 className="text-xl font-bold">Filters</h1>

        <div className="flex flex-col space-y-2 rounded-md border-2  border-blue-700 p-2 pb-4">
          <h3 className="text-lg font-semibold">Date</h3>
          <div className="">
            <label htmlFor="startDate" className=" pr-1.5 font-semibold">
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
            <label htmlFor="endDate" className="pr-3 font-semibold">
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

        <div className="flex flex-col space-y-2 rounded-md border-2 p-2 pb-4">
          <label className="text-lg font-semibold">Distance</label>
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

        <div className="flex flex-col space-y-2 rounded-md border-2 p-2 pb-4">
          <h3 className="text-lg font-semibold">Airport</h3>
          <div className="">
            <h1 className="ml-1 font-semibold">Source</h1>
            <VirtualizedSelect
              value={sourceAirport}
              onChange={setSourceAirport}
              options={airportOptions}
            />
          </div>
          <div className="">
            <h1 className="ml-1 font-semibold">Destination</h1>
            <VirtualizedSelect
              value={destinationAirport}
              onChange={setDestinationAirport}
              options={airportOptions}
            />
          </div>
        </div>

        <div className="flex justify-center">
          <div
            className=" inline-flex w-40 cursor-pointer items-center justify-center rounded-full bg-primary px-10 py-4 text-center font-medium text-white hover:bg-opacity-90 lg:px-8 xl:px-10"
            onClick={(e) => setFilterApplied((prevValue) => prevValue + 1)}
          >
            Apply
          </div>
        </div>
      </aside>

      <div className="rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
        <div className="mb-4 flex items-center ">
          <h4 className=" inline-block text-2xl font-semibold text-black dark:text-white">
            Flights
          </h4>
          <Link
            href="/flights/create"
            className="float-right ml-auto items-center justify-center rounded-md bg-meta-3 px-8 py-4 text-center text-xl font-medium text-white hover:bg-opacity-90 lg:px-6 xl:px-6"
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

          {flights.map((flight, key) => {
            console.log(flight); // Log each flight to the console
            return (
              <Link href={`/flights/${flight.flight_number}`} key={key}>
                <div
                  className={`grid cursor-pointer grid-cols-3 hover:bg-slate-200 dark:hover:bg-meta-4 sm:grid-cols-7 ${
                    key === flights.length - 1
                      ? ""
                      : "border-b border-stroke dark:border-strokedark"
                  }`}
                  key={key}
                >
                  <div className="flex items-center justify-center p-2.5">
                    <div className="flex-shrink-0"></div>
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
                        const hours = date
                          .getHours()
                          .toString()
                          .padStart(2, "0");
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
                      {flight.status}
                    </p>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default FlightTable;
