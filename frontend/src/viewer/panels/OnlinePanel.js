import React, { useEffect, useState, useRef } from "react";
import DirectionPad from '../components/DirectionPad'
import Item from '../components/Item'
import DebugBar from '../components/DebugBar'
import './Panels.css'

export default function OnlinePanel({data, socket}) {
  const [nextTurn, setNextTurn] = useState(0)
  const [timer, setTimer] = useState(0)
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

    const update = () => {
      const now = Date.now() / 1000
      const diff = Math.ceil(data.game.next_turn - now)

      if (diff <= 0) {
        setTimer(0)
        clearInterval(interval.current)
        interval.current = null
      } else {
        setTimer(diff)
      }
    }

    update()
    interval.current = setInterval(update, 100)

    return () => {
      clearInterval(interval.current)
      interval.current = null
    }
  }, [data.game.next_turn])

  return (
    <div>
      {data.game.is_debug && <DebugBar socket={socket}/>}
      <div className="point-bar">
        <div className="stat-item">
          <span className="stat-label">Current Points:</span>
          <span className="stat-value">{data.user.current_points}</span>
        </div>
        <p className="timer-display"><strong>{timer}</strong></p>
        <div className="stat-item">
          <span className="stat-label">Points All-Time:</span>
          <span className="stat-value">{data.user.total_points}</span>
        </div>
      </div>
      <DirectionPad
        data={data}
        socket={socket}
      />
      <div className="balance-container">
        <span className="stat-label">Balance:</span>
        <span className="stat-value">{data.user.balance}</span>
      </div>

      {data.game.shop.map((item, index) => (
        <Item data={item} balance={data.user.balance} socket={socket}/>
      ))}
    </div>
  );
}
