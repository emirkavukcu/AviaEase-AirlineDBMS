// components/Charts/ChartOneDynamic.tsx
import dynamic from "next/dynamic";

const WeatherChartDynamic = dynamic(() => import("./WeatherChart"), {
  ssr: false,
});

export default WeatherChartDynamic;
