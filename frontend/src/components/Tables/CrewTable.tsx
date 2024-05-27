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

const attendantTypeOptions = [
  { value: "chief", label: "Chief" },
  { value: "regular", label: "Regular" },
  { value: "chef", label: "Chef" },
];

const aircraftOptions = [
  { value: 1, label: "Boeing 737" },
  { value: 2, label: "Airbus A320" },
  { value: 3, label: "Boeing 777" },
];

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
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalCount, setTotalCount] = useState<number>(0);

  const [attendantId, setAttendantId] = useState<number | null>(null);
  const [name, setName] = useState<string>("");
  const [minAge, setMinAge] = useState<number | null>(null);
  const [maxAge, setMaxAge] = useState<number | null>(null);
  const [gender, setGender] = useState<string | null>(null);
  const [nationality, setNationality] = useState<string | null>(null);
  const [attendantType, setAttendantType] = useState<string | null>(null);
  const [vehicleTypeIds, setVehicleTypeIds] = useState<number[]>([]);

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
          vehicleTypeIds.forEach((id) => {
            params.append("vehicle_type_ids", id.toString());
          });
        params.append("page", currentPage.toString());
        url.search = params.toString();

        const response = await fetchWithAuth(url.toString());
        const data = await response.json();
        setCrew(data.crew_members);
        setTotalPages(data.pages);
        setTotalCount(data.total);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchCrew();
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
          <label className="pb-2 text-lg font-semibold">Crew ID</label>
          <input
            type="number"
            placeholder="Crew ID"
            value={attendantId || ""}
            className="w-full rounded border p-2"
            onChange={(e) =>
              setAttendantId(e.target.value ? Number(e.target.value) : null)
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
                className="w-full rounded border p-2 text-black"
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
                className="w-full rounded border p-2 text-black"
                onChange={(e) =>
                  setMaxAge(e.target.value ? Number(e.target.value) : null)
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
          <label className="pb-2 text-lg font-semibold">Attendant Type</label>
          <Select
            options={attendantTypeOptions}
            placeholder="Select Attendant"
            onChange={(selectedOption) =>
              setAttendantType(selectedOption ? selectedOption.value : null)
            }
            isClearable
            className="text-black"
          />
        </div>

        <div className="flex flex-col space-y-2 rounded-md border-2 border-blue-800 p-2 pb-4">
          <label className="pb-2 text-lg font-semibold">Aircraft Types</label>
          <Select
            options={aircraftOptions}
            placeholder="Select Aircraft"
            onChange={(selectedOptions) =>
              setVehicleTypeIds(
                selectedOptions
                  ? selectedOptions.map((option) => option.value)
                  : [],
              )
            }
            isMulti
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
        <div className="mb-4 flex items-center justify-between ">
          <h4 className=" inline-block text-2xl font-semibold text-black dark:text-white">
            Crew
          </h4>
          <h4 className="text-2xl font-semibold text-black dark:text-white">
            Total of {totalCount} Crew Members Found
          </h4>
          <Link
            href="/crew/create"
            className="items-center justify-center rounded-md bg-meta-3 px-8 py-4 text-center text-xl font-medium text-white hover:bg-opacity-90 lg:px-6 xl:px-6"
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

          {crew.map((member, key) => (
            <div
              className={`grid grid-cols-3 hover:bg-slate-200 dark:hover:bg-meta-4 sm:grid-cols-8 ${
                key === crew.length - 1
                  ? ""
                  : "border-b border-stroke dark:border-strokedark"
              }`}
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
                <p className="text-center text-black dark:text-white">
                  {member.aircraft_types.map((type, index) => (
                    <span key={index} className="text-black dark:text-white">
                      {type}
                      {index !== member.aircraft_types.length - 1 && ", "}
                    </span>
                  ))}
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

export default CrewTable;
