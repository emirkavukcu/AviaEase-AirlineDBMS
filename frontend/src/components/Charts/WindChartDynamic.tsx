// components/Charts/ChartOneDynamic.tsx
import dynamic from "next/dynamic";

const WindChartDynamic = dynamic(() => import("./WindChart"), {
  ssr: false,
});

export default WindChartDynamic;
