// components/Charts/ChartOneDynamic.tsx
import dynamic from "next/dynamic";

const ChartThreeDynamic = dynamic(() => import("./ChartThree"), {
  ssr: false,
});

export default ChartThreeDynamic;
