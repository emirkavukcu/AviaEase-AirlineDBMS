import DefaultLayout from "@/components/Layouts/DefaultLayout";
import PilotTable from "@/components/Tables/PilotTable";
import React from "react";

const PilotsPage: React.FC = () => {
  return (
    <DefaultLayout>
      <PilotTable />
    </DefaultLayout>
  );
};

export default PilotsPage;
