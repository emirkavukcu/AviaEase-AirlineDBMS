import DefaultLayout from "@/components/Layouts/DefaultLayout";
import CrewTable from "@/components/Tables/CrewTable";
import React from "react";

const CrewPage: React.FC = () => {
  return (
    <DefaultLayout>
      <CrewTable />
    </DefaultLayout>
  );
};

export default CrewPage;
