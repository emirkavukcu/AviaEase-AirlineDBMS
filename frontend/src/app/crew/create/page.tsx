"use client";
import React, { useEffect, useState } from "react";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import Select from "react-select";
import AlertError from "@/components/Alerts/AlertError";
import AlertOk from "@/components/Alerts/AlertOk";
import { get } from "http";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import {
  languageOptions,
  nationalityOptions,
} from "@/components/LanguageData/LanguageData";

const genderOptions = [
  { value: "male", label: "Male" },
  { value: "female", label: "Female" },
];

const vehicleTypeOptions = [
  { value: "Boeing 737", label: "Boeing 737" },
  { value: "Airbus A320", label: "Airbus A320" },
  { value: "Airbus A320", label: "Boeing 777" },
];

const attendantOptions = [
  { value: "chief", label: "Chief" },
  { value: "regular", label: "Regular" },
  { value: "chef", label: "Chef" },
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

const CrewCreationForm = () => {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState<any>(null);
  const [nationality, setNationality] = useState<any>(null);
  const [knownLanguages, setKnownLanguages] = useState<any[]>([]);
  const [vehicleTypes, setVehicleTypes] = useState<any[]>([]);
  const [attendantType, setAttendantType] = useState<any>(null);

  const [alerts, setAlerts] = useState<any[]>([]);
  const [isCreating, setIsCreating] = useState(false);

  const addAlert = (type: string, message: string) => {
    const id = Date.now();
    setAlerts((prevAlerts) => [...prevAlerts, { id, type, message }]);
    setTimeout(() => {
      setAlerts((prevAlerts) => prevAlerts.filter((alert) => alert.id !== id));
    }, 3000);
  };

  const createCrew = async () => {
    if (
      name &&
      age &&
      gender &&
      nationality &&
      knownLanguages.length > 0 &&
      vehicleTypes.length > 0 &&
      attendantType
    ) {
      const ageNumber = parseInt(age, 10);
      if (ageNumber < 18 || ageNumber > 99) {
        addAlert("error", "Age should be between 18-99");
        return;
      }
      setIsCreating(true);

      const response = await fetchWithAuth(
        "http://127.0.0.1:5000/api/create_cabin-crew",
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
            vehicle_type_ids: vehicleTypes.map((type) =>
              getAircraftTypeId(type),
            ),
            attendant_type: attendantType.value,
          }),
        },
      );

      setIsCreating(false);

      if (response.ok) {
        setName("");
        setAge("");
        setGender(null);
        setNationality(null);
        setKnownLanguages([]);
        setVehicleTypes([]);
        setAttendantType(null);
        addAlert("success", "Crew successfully created");
      } else {
        addAlert("error", "Failed to create crew");
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
                Crew Member Creation
              </h3>
            </div>
            <div className="flex flex-col gap-3 p-10 text-lg">
              <div className="flex gap-4">
                <div className="mb-4.5 w-1/2">
                  <label className="mb-3 block font-medium text-black dark:text-white">
                    Name <span className=" text-red">*</span>
                  </label>
                  <input
                    type="text"
                    className="w-full rounded-sm border border-graydark bg-white p-1 dark:border-strokedark dark:bg-boxdark"
                    onChange={(e) => setName(e.target.value)}
                    value={name}
                  />
                </div>

                <div className="mb-4.5 w-1/2">
                  <label className="mb-3 block font-medium text-black dark:text-white">
                    Age <span className=" text-red">*</span>
                  </label>
                  <input
                    placeholder="18-99"
                    type="number"
                    className="w-full rounded-sm border border-graydark bg-white p-1 dark:border-strokedark dark:bg-boxdark"
                    onChange={(e) => setAge(e.target.value)}
                    value={age}
                  />
                </div>
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Gender <span className=" text-red">*</span>
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
                  Nationality <span className=" text-red">*</span>
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
                  Known Languages <span className=" text-red">*</span>
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
                  Attendant Type <span className=" text-red">*</span>
                </label>
                <Select
                  options={attendantOptions}
                  placeholder="Select Attendant Type"
                  onChange={setAttendantType}
                  value={attendantType}
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Aircrafts <span className=" text-red">*</span>
                </label>
                <Select
                  isMulti
                  options={vehicleTypeOptions}
                  placeholder="Select Aircrafts"
                  onChange={(newValue) =>
                    setVehicleTypes(
                      newValue ? newValue.map((l) => l.value) : [],
                    )
                  }
                  value={vehicleTypes.map((lang) => ({
                    value: lang,
                    label: lang,
                  }))}
                />
              </div>

              <button
                className="flex w-full justify-center rounded bg-primary p-3 font-medium text-gray hover:bg-opacity-90 disabled:opacity-50"
                onClick={createCrew}
                disabled={isCreating}
              >
                {isCreating ? "Creating..." : "Create Crew"}
              </button>

              <div className="fixed bottom-5 right-5 space-y-2">
                {alerts.map((alert) =>
                  alert.type === "error" ? (
                    <div
                      key={alert.id}
                      className="opacity-100 transition-opacity duration-1000 ease-out"
                    >
                      <AlertError message={alert.message} />
                    </div>
                  ) : (
                    <div
                      key={alert.id}
                      className="opacity-100 transition-opacity duration-1000 ease-out"
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

export default CrewCreationForm;
