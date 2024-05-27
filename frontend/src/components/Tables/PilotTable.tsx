"use client";
import React, { useState, useEffect } from "react";
import Select from "react-select";
import Link from "next/link";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import { fetchWithAuth } from "@/utils/fetchWithAuth";

const nationalityOptions = [
  { value: "Chinese", label: "Chinese" },
  { value: "Indian", label: "Indian" },
  { value: "American", label: "American" },
  { value: "Indonesian", label: "Indonesian" },
  { value: "Brazilian", label: "Brazilian" },
  { value: "Pakistani", label: "Pakistani" },
  { value: "Nigerian", label: "Nigerian" },
  { value: "Bangladeshi", label: "Bangladeshi" },
  { value: "Russian", label: "Russian" },
  { value: "Japanese", label: "Japanese" },
  { value: "Mexican", label: "Mexican" },
  { value: "Filipino", label: "Filipino" },
  { value: "Egyptian", label: "Egyptian" },
  { value: "Vietnamese", label: "Vietnamese" },
  { value: "Turkish", label: "Turkish" },
  { value: "Iranian", label: "Iranian" },
  { value: "German", label: "German" },
  { value: "Sweden", label: "Sweden" },
  { value: "French", label: "French" },
  { value: "Thai", label: "Thai" },
  { value: "British", label: "British" },
  { value: "Italian", label: "Italian" },
  { value: "South Korean", label: "South Korean" },
  { value: "Colombian", label: "Colombian" },
  { value: "Spanish", label: "Spanish" },
  { value: "Ukrainian", label: "Ukrainian" },
  { value: "Kenyan", label: "Kenyan" },
  { value: "Argentine", label: "Argentine" },
];

const genderOptions = [
  { value: "male", label: "Male" },
  { value: "female", label: "Female" },
];

const seniorityOptions = [
  { value: "senior", label: "Senior" },
  { value: "junior", label: "Junior" },
  { value: "trainee", label: "Trainee" },
];

const aircraftOptions = [
  { value: 1, label: "Boeing 737" },
  { value: 2, label: "Airbus A320" },
  { value: 3, label: "Boeing 777" },
];

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
  const [pilots, setPilots] = useState<Pilot[]>([]);
  const [filterApplied, setFilterApplied] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalCount, setTotalCount] = useState<number>(0);

  const [pilotId, setPilotId] = useState<number | null>(null);
  const [name, setName] = useState<string>("");
  const [minAge, setMinAge] = useState<number | null>(null);
  const [maxAge, setMaxAge] = useState<number | null>(null);
  const [gender, setGender] = useState<string | null>(null);
  const [nationality, setNationality] = useState<string | null>(null);
  const [minAllowedRange, setMinAllowedRange] = useState<number | null>(null);
  const [maxAllowedRange, setMaxAllowedRange] = useState<number | null>(null);
  const [seniorityLevel, setSeniorityLevel] = useState<string | null>(null);
  const [aircraftType, setAircraftType] = useState<number | null>(null);

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
        if (aircraftType)
          params.append("vehicle_type_id", aircraftType.toString());
        if (seniorityLevel) params.append("seniority_level", seniorityLevel);

        params.append("page", currentPage.toString());

        url.search = params.toString();

        const response = await fetchWithAuth(url.toString());
        const data = await response.json();
        setPilots(data.pilots);
        setTotalPages(data.pages);
        setTotalCount(data.total);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchPilots();
  }, [filterApplied, currentPage]);

  const handleFilterApply = () => {
    setCurrentPage(1);
    setFilterApplied((prevValue) => prevValue + 1);
  };

  const handlePageChange = (
    event: React.ChangeEvent<unknown>,
    value: number,
  ) => {
    setCurrentPage(value);
  };

  return (
    <div className="flex">
      <aside className="flex w-64 flex-col gap-y-2 bg-slate-50 p-4 pt-10 text-black dark:border-strokedark dark:bg-boxdark dark:text-white">
        <h1 className="pb-4 text-2xl font-bold">Filters</h1>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Pilot ID</label>
          <input
            type="number"
            placeholder="Pilot ID"
            value={pilotId || ""}
            className="w-full rounded border p-2"
            onChange={(e) =>
              setPilotId(e.target.value ? Number(e.target.value) : null)
            }
          />
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Name</label>
          <input
            type="text"
            placeholder="Name"
            value={name}
            className="w-full rounded border p-2"
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="text-lg font-semibold">Age</label>
          <div className="flex items-center space-x-2">
            <div className="flex flex-col">
              <label className="text-md pb-1">Min</label>
              <input
                type="number"
                placeholder="Min"
                value={minAge || ""}
                className="w-full rounded border p-2"
                onChange={(e) =>
                  setMinAge(e.target.value ? Number(e.target.value) : null)
                }
              />
            </div>
            <span className="pt-6 font-bold">-</span>
            <div className="flex flex-col">
              <label className="text-md pb-1">Max</label>
              <input
                type="number"
                placeholder="Max"
                value={maxAge || ""}
                className="w-full rounded border p-2"
                onChange={(e) =>
                  setMaxAge(e.target.value ? Number(e.target.value) : null)
                }
              />
            </div>
          </div>
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="text-lg font-semibold">Range</label>
          <div className="flex items-center space-x-2">
            <div className="flex flex-col">
              <label className="text-md pb-1">Min</label>
              <input
                type="number"
                placeholder="Min"
                value={minAllowedRange || ""}
                className="w-full rounded border p-2 text-black"
                onChange={(e) =>
                  setMinAllowedRange(
                    e.target.value ? Number(e.target.value) : null,
                  )
                }
              />
            </div>
            <span className="pt-6 font-bold">-</span>
            <div className="flex flex-col">
              <label className="text-md pb-1 text-black">Max</label>
              <input
                type="number"
                placeholder="Max"
                value={maxAllowedRange || ""}
                className="w-full rounded border p-2"
                onChange={(e) =>
                  setMaxAllowedRange(
                    e.target.value ? Number(e.target.value) : null,
                  )
                }
              />
            </div>
          </div>
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Gender</label>
          <Select
            options={genderOptions}
            placeholder="Select Gender"
            onChange={(selectedOption) =>
              setGender(selectedOption ? selectedOption.value : null)
            }
            isClearable
            className="text-black"
          />
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Nationality</label>
          <Select
            options={nationalityOptions}
            placeholder="Select Nationality"
            onChange={(selectedOption) =>
              setNationality(selectedOption ? selectedOption.value : null)
            }
            isClearable
            className="text-black"
          />
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Seniority Level</label>
          <Select
            options={seniorityOptions}
            placeholder="Select Seniority"
            onChange={(selectedOption) =>
              setSeniorityLevel(selectedOption ? selectedOption.value : null)
            }
            isClearable
            className="text-black"
          />
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Aircraft</label>
          <Select
            options={aircraftOptions}
            placeholder="Select Aircraft"
            onChange={(selectedOption) =>
              setAircraftType(selectedOption ? selectedOption.value : null)
            }
            isClearable
            className="text-black"
          />
        </div>

        <div className="flex justify-center">
          <div
            className="inline-flex w-50 cursor-pointer items-center justify-center rounded-full bg-primary px-4 py-4 text-center text-lg font-medium text-white hover:bg-opacity-90"
            onClick={handleFilterApply}
          >
            Apply Filters
          </div>
        </div>
      </aside>

      <div className="w-full rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
        <div className="mb-4 flex items-center justify-between">
          <h4 className=" inline-block text-2xl font-semibold text-black dark:text-white">
            Pilots
          </h4>
          <h4 className="text-2xl font-semibold text-black dark:text-white">
            Total of {totalCount} Pilots Found
          </h4>
          <Link
            href="/pilots/create"
            className="items-center justify-center rounded-md bg-meta-3 px-8 py-4 text-center text-xl font-medium text-white hover:bg-opacity-90 lg:px-6 xl:px-6"
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
            <div className=" p-2.5 xl:p-5">
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

          {pilots.map((pilot, key) => (
            <div
              className={`grid grid-cols-3 hover:bg-slate-200 dark:hover:bg-meta-4 sm:grid-cols-9 ${
                key === pilots.length - 1
                  ? ""
                  : "border-b border-stroke dark:border-strokedark"
              }`}
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
                  {pilot.gender.charAt(0).toUpperCase() + pilot.gender.slice(1)}
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

export default PilotTable;
