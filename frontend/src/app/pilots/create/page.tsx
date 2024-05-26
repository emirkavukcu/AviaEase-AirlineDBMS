"use client";
import React, { useEffect, useState } from "react";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import Select from "react-select";
import AlertError from "@/components/Alerts/AlertError";
import AlertOk from "@/components/Alerts/AlertOk";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import {
  languageOptions,
  nationalityOptions,
} from "@/components/LanguageData/LanguageData";

const genderOptions = [
  { value: "Male", label: "Male" },
  { value: "Female", label: "Female" },
];

const vehicleTypeOptions = [
  { value: 1, label: "Boeing 737" },
  { value: 2, label: "Airbus A320" },
  { value: 3, label: "Boeing 777" },
];

const rangeOptions = [
  { value: 2000, label: "2000" },
  { value: 5000, label: "5000" },
  { value: 10000, label: "10000" },
  { value: 15000, label: "15000" },
  { value: 20000, label: "20000" },
];

const seniorityOptions = [
  { value: "Senior", label: "Senior" },
  { value: "Junior", label: "Junior" },
  { value: "Trainee", label: "Trainee" },
];

const getAircraftTypeId = (aircraftType: string) => {
  switch (aircraftType) {
    case "Airbus A320":
      return 2;
    case "Boeing 737":
      return 1;
    case "Boeing 777":
      return 3;
    default:
      return null;
  }
};

const PilotCreationForm = () => {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState<any>(null);
  const [nationality, setNationality] = useState<any>([]);
  const [knownLanguages, setKnownLanguages] = useState<any[]>([]);
  const [vehicleType, setVehicleType] = useState<any>(null);
  const [allowedRange, setAllowedRange] = useState<any>(null);
  const [seniorityLevel, setSeniorityLevel] = useState<any>(null);

  const [alerts, setAlerts] = useState<any[]>([]);
  const [isCreating, setIsCreating] = useState(false);

  const addAlert = (type: string, message: string) => {
    const id = Date.now();
    setAlerts((prevAlerts) => [...prevAlerts, { id, type, message }]);
    setTimeout(() => {
      setAlerts((prevAlerts) => prevAlerts.filter((alert) => alert.id !== id));
    }, 3000);
  };

  const createPilot = async () => {
    if (
      name &&
      age &&
      gender &&
      nationality &&
      knownLanguages.length > 0 &&
      vehicleType &&
      allowedRange &&
      seniorityLevel
    ) {
      const ageNumber = parseInt(age, 10);
      if (ageNumber < 18 || ageNumber > 99) {
        addAlert("error", "Age should be between 18-99");
        return;
      }
      setIsCreating(true);

      const response = await fetchWithAuth(
        "http://127.0.0.1:5000/api/create_pilot",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name,
            age: parseInt(age, 10),
            gender: gender.value,
            nationality: nationality.value,
            known_languages: knownLanguages,
            vehicle_type_id: vehicleType.value,
            allowed_range: allowedRange.value,
            seniority_level: seniorityLevel.value.toLowerCase(),
          }),
        },
      );

      setIsCreating(false);

      if (response.ok) {
        setName("");
        setAge("");
        setGender(null);
        setNationality([]);
        setKnownLanguages([]);
        setVehicleType(null);
        setAllowedRange(null);
        setSeniorityLevel(null);
        addAlert("success", "Pilot successfully created");
      } else {
        addAlert("error", "Failed to create pilot");
      }
    } else {
      addAlert("error", "All fields must be filled");
    }
  };

  return (
    <DefaultLayout>
      <div className="flex justify-center">
        <div className="flex w-1/2 flex-col">
          <div className="grayinputs rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
            <div className="border-b border-stroke px-10 py-4 dark:border-strokedark">
              <h3 className="text-2xl font-medium text-black dark:text-white">
                Pilot Creation
              </h3>
            </div>
            <div className="flex flex-col gap-3 p-10 text-lg shadow-default">
              <div className="flex gap-4 ">
                <div className="mb-4.5 w-1/2">
                  <label className="mb-3 block font-medium text-black dark:text-white">
                    Name
                  </label>
                  <input
                    type="text"
                    className="w-full rounded-sm border border-graydark bg-white p-1  dark:border-strokedark dark:bg-boxdark"
                    onChange={(e) => setName(e.target.value)}
                    value={name}
                  />
                </div>

                <div className="mb-4.5 w-1/2">
                  <label className="mb-3 block font-medium text-black dark:text-white">
                    Age
                  </label>
                  <input
                    placeholder="18-99"
                    type="number"
                    className="w-full rounded-sm border border-graydark bg-white p-1  dark:border-strokedark dark:bg-boxdark"
                    onChange={(e) => setAge(e.target.value)}
                    value={age}
                  />
                </div>
              </div>

              <div className="mb-4.5 ">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Gender
                </label>
                <Select
                  options={genderOptions}
                  placeholder="Select Gender"
                  onChange={setGender}
                  value={gender}
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Nationality
                </label>
                <Select
                  options={nationalityOptions}
                  placeholder="Select Nationality"
                  onChange={setNationality}
                  value={nationality}
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Known Languages
                </label>
                <Select
                  options={languageOptions}
                  isMulti
                  defaultValue={[]}
                  placeholder="Select Known Languages"
                  onChange={(newValue) =>
                    setKnownLanguages(
                      newValue ? newValue.map((l) => l.value) : [],
                    )
                  }
                  value={knownLanguages.map((lang) => ({
                    value: lang,
                    label: lang,
                  }))}
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Aircraft Type
                </label>
                <Select
                  options={vehicleTypeOptions}
                  placeholder="Select Aircraft Type"
                  onChange={setVehicleType}
                  value={vehicleType}
                  className=""
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Allowed Range
                </label>
                <Select
                  options={rangeOptions}
                  placeholder="Select Allowed Range"
                  onChange={setAllowedRange}
                  value={allowedRange}
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Seniority Level
                </label>
                <Select
                  options={seniorityOptions}
                  placeholder="Select Seniority Level"
                  onChange={setSeniorityLevel}
                  value={seniorityLevel}
                />
              </div>

              <button
                className="flex w-full justify-center rounded bg-primary p-3 font-medium text-gray hover:bg-opacity-90 disabled:opacity-50"
                onClick={createPilot}
                disabled={isCreating}
              >
                {isCreating ? "Creating..." : "Create Pilot"}
              </button>

              <div className="fixed bottom-5 right-5 space-y-2">
                {alerts.map((alert) =>
                  alert.type === "error" ? (
                    <div
                      key={alert.id}
                      className="w-100 opacity-100 transition-opacity duration-1000 ease-out"
                    >
                      <AlertError message={alert.message} />
                    </div>
                  ) : (
                    <div
                      key={alert.id}
                      className="w-100 opacity-100 transition-opacity duration-1000 ease-out"
                    >
                      <AlertOk message={alert.message} />
                    </div>
                  ),
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </DefaultLayout>
  );
};

export default PilotCreationForm;
