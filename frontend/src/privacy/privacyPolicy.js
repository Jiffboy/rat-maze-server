import React from 'react'
import './privacyPolicy.css'

export default function PrivacyPolicy() {
    return <div className="privacy-policy">
        <h1>Privacy Policy</h1>
        <p>Rat Maze stores data only as is necessary to operate. This includes exclusively the following:</p>
        <ul>
            <li>Twitch Username</li>
            <li>Twitch User Id</li>
            <li>User interaction with the widget</li>
        </ul>
        <p>The collection of this data is opt-in <strong>only</strong>, and may once more be opted out thereafter via the twitch extension. The user shall be given an anonymous name while opted out, although user interactions with the widget will still be tracked. User interaction data is tracked as follows:</p>
        <ul>
            <li>Any interactions prior to linking with twitch will be migrated to link to the user's id and username once opted in.</li>
            <li>Should the user opt out after opting in, they will be given a new anonymous name detatched from previous interaction data.</li>
            <li>Should the user opt in once more thereafter, all data underneath this new anonymous name will <strong>not</strong> be migrated to the user's id, and shall be considered separate, due to the anonymous nature of these interactions.</li>
            <li>All data will be retained indefinitely regardless of opting out. If you wish for this data to be expunged, please contact <a href="https://www.twitch.tv/jiffboy">Jiffboy</a> on Twitch. </li>
        </ul>
        <p>As Rat Maze operates within Twitch, please additionally review Twitch's <a href="https://legal.twitch.com/en/legal/privacy-notice/">Privacy Policy</a>.</p>
    </div>
}