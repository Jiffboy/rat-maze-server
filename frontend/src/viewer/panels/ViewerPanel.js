import React, { useEffect, useState, useRef } from "react";
import OnlinePanel from './OnlinePanel'
import OfflinePanel from './OfflinePanel'
import loadingImg from '../../assets/loading.gif';
import { io } from 'socket.io-client'

export default function ViewerPanel() {
  const [data, setData] = useState(null)
  const socket = useRef(null)

  useEffect(() => {
    if (window.Twitch && window.Twitch.ext) {
      window.Twitch.ext.onAuthorized((auth) => {
        if (auth?.userId) {
          socket.current = io(process.env.REACT_APP_API_URL + "/ratmaze/widget", {
            path: "/socket.io",
            transports: ["websocket", "polling"],
            auth: { token: auth.token }
          });

          socket.current.on("data_update", (payload) => {
            setData(payload)
          })
        }
      });
    }
  }, []);

  return (
  <div>
    {!data &&
        <div className='loading-container'>
          <div>
            <img className='loading-img' src={loadingImg}/>
            <p>Loading...</p>
          </div>
        </div>
    }
    {data && !data.user.permission_granted &&
      <div className="warning-banner">
        <p>You have been given the anonymous name: <strong>{data.user.username}</strong></p>
        <p>To share your username, click the button at the bottom of this panel.</p>
      </div>
    }

    {data && data.game.is_live && <OnlinePanel data={data} socket={socket}/>}
    {data && !data.game.is_live && <OfflinePanel data={data} socket={socket}/>}
  </div>
  )
}