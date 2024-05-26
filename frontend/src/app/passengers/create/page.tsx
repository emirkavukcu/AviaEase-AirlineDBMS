"use client";
import React, { useState } from "react";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import Select from "react-select";
import AlertError from "@/components/Alerts/AlertError";
import AlertOk from "@/components/Alerts/AlertOk";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { nationalityOptions } from "@/components/LanguageData/LanguageData";

const genderOptions = [
  { value: "male", label: "Male" },
  { value: "female", label: "Female" },
];

const PassengerCreationForm = () => {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState<any>(null);
  const [nationality, setNationality] = useState<any>(null);
  const [parentId, setParentId] = useState<any>(null);
  const [affiliates, setAffiliates] = useState<string>("");

  const [alerts, setAlerts] = useState<any[]>([]);
  const [isCreating, setIsCreating] = useState(false);

  const addAlert = (type: string, message: string) => {
    const id = Date.now();
    setAlerts((prevAlerts) => [...prevAlerts, { id, type, message }]);
    setTimeout(() => {
      setAlerts((prevAlerts) => prevAlerts.filter((alert) => alert.id !== id));
    }, 3000);
  };

  const parseAffiliates = (input: string) => {
    return input
      .split(",")
      .map((item) => parseInt(item.trim(), 10))
      .filter((item) => !isNaN(item));
  };

  const validateAffiliates = (affiliates: number[]) => {
    if (affiliates.length > 2) {
      addAlert("error", "You can only select up to 2 affiliates.");
      return false;
    }
    if (affiliates.some((item) => item < 1 || item > 20000)) {
      addAlert("error", "Affiliates must be integers between 1 and 20000.");
      return false;
    }
    return true;
  };

  const createPassenger = async () => {
    if (name && age && gender && nationality) {
      const parsedAffiliates = parseAffiliates(affiliates);
      if (affiliates && !validateAffiliates(parsedAffiliates)) {
        return;
      }

      if (parseInt(age, 10) < 3) {
        if (!parentId || parentId < 1 || parentId > 20000) {
          addAlert("error", "Invalid Parent Id");
          return;
        }
      }
      const ageNumber = parseInt(age, 10);
      if (ageNumber < 0 || ageNumber > 99) {
        addAlert("error", "Age should be between 18-99");
        return;
      }

      setIsCreating(true);

      const passengerData = {
        name,
        age: parseInt(age, 10),
        gender: gender.value,
        nationality: nationality.value,
        parent_id: null,
        affiliated_passenger_ids: parsedAffiliates,
      };

      if (parseInt(age, 10) < 3) {
        passengerData["parent_id"] = parentId;
      }

      console.log(passengerData);

      const response = await fetchWithAuth(
        "http://127.0.0.1:5000/api/create_passenger",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(passengerData),
        },
      );

      setIsCreating(false);

      if (response.ok) {
        setName("");
        setAge("");
        setGender(null);
        setNationality(null);
        setParentId(null);
        setAffiliates("");
        addAlert("success", "Passenger successfully created");
      } else {
        addAlert("error", "Failed to create passenger");
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
                Passenger Creation
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
                    placeholder="0-99"
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
                  Affiliates
                </label>
                <input
                  type="text"
                  className="w-full rounded-sm border border-graydark bg-white p-1 shadow-default dark:border-strokedark dark:bg-boxdark"
                  onChange={(e) => setAffiliates(e.target.value)}
                  value={affiliates}
                  placeholder="Enter comma-separated values (e.g. 1, 2, 3)"
                />
              </div>

              {parseInt(age, 10) < 3 && (
                <div className="mb-4.5">
                  <label className="mb-3 block font-medium text-black dark:text-white">
                    Parent Id <span className=" text-red">*</span>
                  </label>
                  <input
                    type="number"
                    className="w-full rounded-sm border border-graydark bg-white p-1 shadow-default dark:border-strokedark dark:bg-boxdark"
                    onChange={(e) => setParentId(parseInt(e.target.value, 10))}
                    value={parentId || ""}
                  />
                </div>
              )}

              <button
                className="flex w-full justify-center rounded bg-primary p-3 font-medium text-gray hover:bg-opacity-90 disabled:opacity-50"
                onClick={createPassenger}
                disabled={isCreating}
              >
                {isCreating ? "Creating..." : "Create Passenger"}
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

export default PassengerCreationForm;
