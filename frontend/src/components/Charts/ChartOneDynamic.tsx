// components/Charts/ChartOneDynamic.tsx
import dynamic from "next/dynamic";

const ChartOneDynamic = dynamic(() => import("./ChartOne"), {
  ssr: false,
});

export default ChartOneDynamic;
