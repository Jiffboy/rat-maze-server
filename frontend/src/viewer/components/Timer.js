import React, { useState, useEffect, useRef } from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css';

export default function Timer({data}) {
  const [timer, setTimer] = useState(0)
  const [percent, setPercent] = useState(0)
  const [timerRunning, setTimerRunning] = useState(false)
  const interval = useRef(null)

  useEffect(() => {
    if (interval.current) {
      clearInterval(interval.current)
      interval.current = null;
    }

    if (!data.game.next_turn) {
      setTimer(0)
      return
    }

    // Sometimes there is drift compared to local systems, so we make sure it does not exceed
    // the length of the turn.
    const nextTurn = Math.min(data.game.next_turn, (Date.now() / 1000) + data.game.turn_length)
    const pastTurn = Date.now() / 1000

    const update = () => {
      const now = Date.now() / 1000
      const diff = Math.ceil(nextTurn - now)
      const maxVal = nextTurn - pastTurn
      const currVal = nextTurn - now
      setPercent(currVal / maxVal)
      if (diff <= 0) {
        setTimer(0)
        clearInterval(interval.current)
        interval.current = null
      } else {
        setTimer(diff)
      }
    }

    update()
    interval.current = setInterval(update, 50)

    return () => {
      clearInterval(interval.current)
      interval.current = null
    }
  }, [data.game.next_turn])

  return (
    <div className="timer">
      <CircularProgressbar value={percent} maxValue={1} strokeWidth={50} styles={buildStyles({ pathTransition: 'none', pathColor: "white", trailColor: "transparent", strokeLinecap: "butt" })}/>
    </div>
  );
};