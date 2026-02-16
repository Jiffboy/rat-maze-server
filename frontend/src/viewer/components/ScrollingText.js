import React, {useState, useEffect} from 'react';
import './ScrollingText.css';

export default function ScrollingText({data, text, show}) {
  const [bgColor, setBgColor] = useState("transparent");
  const [inAnimation, setInAnimation] = useState(false);
  const [key, setKey] = useState("")

  useEffect(() => {
    if (show) {
      setBgColor("#000000BB")
      setInAnimation(true)
      setKey(Date.now() + text)
    }
    console.log(show)
  }, [show])
  return (
    <ScrollBanner key={key} text={text} bgColor={bgColor} setBgColor={setBgColor} inAnimation={inAnimation} setInAnimation={setInAnimation}/>
  );
};

function ScrollBanner({text, show, bgColor, setBgColor, inAnimation, setInAnimation}) {
  const handleAnimationEnd = () => {
    setBgColor("transparent");
    setInAnimation(false)
  };

  return (
    <div className="scroll-container" style={{ backgroundColor: bgColor }}>
      {inAnimation &&
      <div className="scroll-text" onAnimationEnd={handleAnimationEnd}>
        {text}
      </div>}
    </div>
  )
}