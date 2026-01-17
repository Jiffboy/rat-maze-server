import React, { useEffect, useState, useRef } from "react";
import DirectionPad from '../components/DirectionPad'
import Item from '../components/Item'

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
      <div className="point-bar">
        <p><strong>Points:</strong> {data.user.current_points}</p>
        <p><strong>{timer}</strong></p>
        <p><strong>Total:</strong> {data.user.total_points}</p>
      </div>
      <DirectionPad
        data={data}
        socket={socket}
      />
      <hr/>
      <p><strong>Balance:</strong> {data.user.balance}</p>

      {data.game.shop.map((item, index) => (
        <Item data={item} balance={data.user.balance} socket={socket}/>
      ))}
    </div>
  );
}