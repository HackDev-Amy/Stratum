import { useEffect, useRef, useState } from "react";

export default function Price({ value, prefix = "$", decimals = 2, className = "" }) {
  const prev = useRef(value);
  const [flash, setFlash] = useState("");

  useEffect(() => {
    if (prev.current !== value) {
      setFlash(value > prev.current ? "animate-flashUp" : "animate-flashDown");
      prev.current = value;
      const t = setTimeout(() => setFlash(""), 600);
      return () => clearTimeout(t);
    }
  }, [value]);

  return (
    <span className={`num ${className} ${flash} rounded px-1`}>
      {prefix}
      {Number(value).toLocaleString(undefined, {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
      })}
    </span>
  );
}