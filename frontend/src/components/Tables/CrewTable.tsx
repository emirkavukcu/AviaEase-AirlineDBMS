"use client";
import React, { useState, useEffect } from "react";
import Select from "react-select";
import VirtualizedSelect from "./VirtualizedSelect";
import Link from "next/link";

interface Crew {
  attendant_id: number;
  age: number;
  gender: string;
  name: string;
  nationality: string;
  attendant_type: string;
  known_languages: string[];
  aircraft_types: string[];
  vehicle_type_ids: number[];
}

const CrewTable = () => {
  const [crew, setCrew] = useState<Crew[]>([]);
  const [filterApplied, setFilterApplied] = useState<number>(0);

  useEffect(() => {
    const fetchCrew = async () => {
      try {
        let url = new URL("http://127.0.0.1:5000/api/cabin-crew");
        let params = new URLSearchParams();

        if (attendantId) params.append("attendant_id", attendantId.toString());
        if (name) params.append("name", name);
        if (minAge) params.append("min_age", minAge.toString());
        if (maxAge) params.append("max_age", maxAge.toString());
        if (gender) params.append("gender", gender);
        if (nationality) params.append("nationality", nationality);
        if (attendantType) params.append("attendant_type", attendantType);
        if (vehicleTypeIds.length > 0)
          params.append("vehicle_type_ids", JSON.stringify(vehicleTypeIds));

        url.search = params.toString();

        const response = await fetch(url.toString());
        const data = await response.json();
        setCrew(data.crew_members);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchCrew();
  }, [filterApplied]);

  const [attendantId, setAttendantId] = useState<number | null>(null);
  const [name, setName] = useState<string>("");
  const [minAge, setMinAge] = useState<number | null>(null);
  const [maxAge, setMaxAge] = useState<number | null>(null);
  const [gender, setGender] = useState<string>("");
  const [nationality, setNationality] = useState<string>("");
  const [attendantType, setAttendantType] = useState<string>("");
  const [vehicleTypeIds, setVehicleTypeIds] = useState<number[]>([]);

  return (
    <div className="flex">
      <aside className="flex w-64 flex-col gap-y-2 p-4 text-black">
        <h1 className="text-xl font-bold">Filters</h1>
      </aside>

      <div className="rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
        <div className="mb-4 flex items-center ">
          <h4 className=" inline-block text-2xl font-semibold text-black dark:text-white">
            Crew
          </h4>
          <Link
            href=""
            className="float-right ml-auto items-center justify-center rounded-md bg-meta-3 px-8 py-4 text-center text-xl font-medium text-white hover:bg-opacity-90 lg:px-6 xl:px-6"
          >
            Create Crew
          </Link>
        </div>
        <div className="flex flex-col">
          <div className="grid grid-cols-3 rounded-sm bg-gray-2 dark:bg-meta-4 sm:grid-cols-8">
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
                Type
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
                Aircrafts
              </h5>
            </div>
          </div>

          {crew.map((member, key) => {
            return (
              <Link href={`/`} key={key}>
                <div
                  className={`grid cursor-pointer grid-cols-3 hover:bg-slate-200 dark:hover:bg-meta-4 sm:grid-cols-8 ${
                    key === crew.length - 1
                      ? ""
                      : "border-b border-stroke dark:border-strokedark"
                  }`}
                  key={key}
                >
                  <div className="flex items-center justify-center p-2.5">
                    <div className="flex-shrink-0"></div>
                    <p className="hidden text-black dark:text-white sm:block">
                      {member.attendant_id}
                    </p>
                  </div>
                  <div className="flex items-center justify-center p-2.5">
                    <p className="text-center text-black dark:text-white">
                      {member.name}
                    </p>
                  </div>

                  <div className="flex items-center justify-center p-2.5">
                    <p className="text-black dark:text-white">{member.age}</p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-black dark:text-white">
                      {member.gender.charAt(0).toUpperCase() +
                        member.gender.slice(1)}
                    </p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-black dark:text-white">
                      {member.attendant_type.charAt(0).toUpperCase() +
                        member.attendant_type.slice(1)}
                    </p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-black dark:text-white">
                      {member.nationality}
                    </p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-center text-black dark:text-white">
                      {member.known_languages.join(", ")}
                    </p>
                  </div>

                  <div className="hidden items-center justify-center p-2.5 sm:flex">
                    <p className="text-black dark:text-white">
                      {member.aircraft_types.map((type, index) => (
                        <p key={index} className="text-black dark:text-white">
                          {type}
                        </p>
                      ))}
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

export default CrewTable;
