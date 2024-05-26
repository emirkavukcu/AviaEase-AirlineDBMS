import React from "react";
import Select from "react-select";
import { FixedSizeList as List } from "react-window";

const height = 35;

const MenuList = (props: { options: any; children: any; getValue: any }) => {
  const { options, children, getValue } = props;
  const [value] = getValue();
  const initialOffset = options.indexOf(value) * height;

  return (
    <List
      width={150}
      height={height * 5}
      itemCount={children.length}
      itemSize={height}
      initialScrollOffset={initialOffset}
    >
      {({ index, style }) => <div style={style}>{children[index]}</div>}
    </List>
  );
};

const VirtualizedSelect = (props: any) => (
  <Select {...props} components={{ MenuList }} />
);

export default VirtualizedSelect;
