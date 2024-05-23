"use client";
import React, { useState, useEffect } from "react";
import Select from "react-select";
import VirtualizedSelect from "./VirtualizedSelect";
import Link from "next/link";

interface Pilot {
  pilot_id: number;
  age: number;
  gender: string;
  name: string;
  allowed_range: number;
  seniority_level: string;
  known_languages: string[];
  vehicle_type_id: number;
  aircraft_type: string;
  nationality: string;
  scheduled_flights: number[];
}

const PilotTable = () => {
  const [pilots, setPilots] = useState<Pilot[]>([]); // This should be fetched or passed as props
  const [filterApplied, setFilterApplied] = useState<number>(0);

  useEffect(() => {
    const fetchPilots = async () => {
      try {
        let url = new URL("http://127.0.0.1:5000/api/pilots");
        let params = new URLSearchParams();

        if (pilotId) params.append("pilot_id", pilotId.toString());
        if (name) params.append("name", name);
        if (minAge) params.append("min_age", minAge.toString());
        if (maxAge) params.append("max_age", maxAge.toString());
        if (gender) params.append("gender", gender);
        if (nationality) params.append("nationality", nationality);
        if (minAllowedRange)
          params.append("min_allowed_range", minAllowedRange.toString());
        if (maxAllowedRange)
          params.append("max_allowed_range", maxAllowedRange.toString());
        if (aircraftType) params.append("aircraft_type", aircraftType);

        if (seniorityLevel) params.append("seniority_level", seniorityLevel);

        url.search = params.toString();

        const response = await fetch(url.toString());
        const data = await response.json();
        setPilots(data.pilots);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchPilots();
  }, [filterApplied]);

  const [pilotId, setPilotId] = useState<number | null>(null);
  const [name, setName] = useState<string>("");
  const [minAge, setMinAge] = useState<number | null>(null);
  const [maxAge, setMaxAge] = useState<number | null>(null);
  const [gender, setGender] = useState<string>("");
  const [nationality, setNationality] = useState<string>("");
  const [minAllowedRange, setMinAllowedRange] = useState<number | null>(null);
  const [maxAllowedRange, setMaxAllowedRange] = useState<number | null>(null);
  const [seniorityLevel, setSeniorityLevel] = useState<string>("");
  const [aircraftType, setAircraftType] = useState<string>("");

  return (
    <div className="flex">
      <aside className="flex w-64 flex-col gap-y-2 p-4 text-black">
        <h1 className="text-xl font-bold">Filters</h1>
      </aside>

      <div className="rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
        <div className="mb-4 flex items-center ">
          <h4 className=" inline-block text-2xl font-semibold text-black dark:text-white">
            Pilots
          </h4>
          <Link
            href="/"
            className="float-right ml-auto items-center justify-center rounded-md bg-meta-3 px-8 py-4 text-center text-xl font-medium text-white hover:bg-opacity-90 lg:px-6 xl:px-6"
          >
            Create Pilot
          </Link>
        </div>
        <div className="flex flex-col">
          <div className="grid grid-cols-3 rounded-sm bg-gray-2 dark:bg-meta-4 sm:grid-cols-9">
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Id
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Name
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Age
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Gender
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Seniority
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Range
              </h5>
            </div>
            <div className="hidden p-2.5 sm:block xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Nationality
              </h5>
            </div>
            <div className="hidden p-2.5 sm:block xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Languages
              </h5>
            </div>
            <div className="hidden p-2.5 sm:block xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Aircraft
              </h5>
            </div>
          </div>

          {pilots.map((pilot, key) => {
            console.log(pilot); // Log each pilot to the console
            return (
              <Link href={`/`} key={key}>
                <div
                  className={`grid cursor-pointer grid-cols-3 hover:bg-slate-200 dark:hover:bg-meta-4 sm:grid-cols-9 ${
                    key === pilots.length - 1
                      ? ""
                      : "border-b border-stroke dark:border-strokedark"
                  }`}
                  key={key}
                >
                  <div className="flex items-center justify-center p-2.5">
                    <div className="flex-shrink-0"></div>
                    <p className="hidden text-black dark:text-white sm:block">
                      {pilot.pilot_id}
                    </p>
                  </div>
                  <div className="flex items-center justify-center p-2.5">
                    <p className="text-center text-black dark:text-white">
                      {pilot.name}
                    </p>
                  </div>

                  <div className="flex items-center justify-center p-2.5">
                    <p className="text-black dark:text-white">{pilot.age}</p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-black dark:text-white">
                      {" "}
                      {pilot.gender.charAt(0).toUpperCase() +
                        pilot.gender.slice(1)}
                    </p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-black dark:text-white">
                      {pilot.seniority_level.charAt(0).toUpperCase() +
                        pilot.seniority_level.slice(1)}
                    </p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-black dark:text-white">
                      {pilot.allowed_range}
                    </p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-black dark:text-white">
                      {pilot.nationality}
                    </p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-center text-black dark:text-white">
                      {pilot.known_languages.join(", ")}
                    </p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-black dark:text-white">
                      {pilot.aircraft_type}
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

export default PilotTable;
