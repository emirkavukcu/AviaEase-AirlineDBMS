import DefaultLayout from "@/components/Layouts/DefaultLayout";
import FlightTable from "@/components/Tables/FlightTable";
import React from "react";

const FlightsPage: React.FC = () => {
  return (
    <DefaultLayout>
      <FlightTable />
    </DefaultLayout>
  );
};

export default FlightsPage;
