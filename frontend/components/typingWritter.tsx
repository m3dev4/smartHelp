import { useEffect, useState } from "react";

interface TypingWritterProps {
  texte: string;
  speed?: number;
}

const TypingWritter = ({ texte, speed }: TypingWritterProps) => {
  const [displayed, setDisplayed] = useState("");
  useEffect(() => {
    let index = 0;

    const interval = setInterval(() => {
      setDisplayed(texte.slice(0, index + 1));
      index++;

      if (index >= texte.length) {
        clearInterval(interval);
      }
    }, speed || 100);
  }, [texte, speed]);
  return <span>{displayed}</span>;
};

export default TypingWritter;
