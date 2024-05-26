import DefaultLayout from "@/components/Layouts/DefaultLayout";
import PassengerTable from "@/components/Tables/PassengerTable";
import React from "react";

const PassengersPage: React.FC = () => {
  return (
    <DefaultLayout>
      <PassengerTable />
    </DefaultLayout>
  );
};

export default PassengersPage;
