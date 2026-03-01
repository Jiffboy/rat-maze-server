import React from 'react'
import './tos.css'

export default function TermsOfService() {
    return <div className="terms-of-service">
        <h1>Terms Of Service</h1>
        <p> By using the Widget, the User agrees to be bound by the terms of this Agreement. If the User does not agree to the terms of this Agreement, they should immediately discontinue use of the Widget. </p>
            <ol>
                <li className='tos-list-item'>
                    <font color="darkred">Use of the Widget: </font>
                    The Widget Owner grants the User a non-exclusive, non-transferable, limited license to use the Widget for personal or non-commercial purposes.
                </li>
                <li className='tos-list-item'>
                    <font color="darkred">Prohibited Use: </font>
                    The User may not use the Widget in any way that violates applicable laws, rules, or regulations or infringes upon the rights of any third party. The User may not use the Widget for any commercial purposes without the express written consent of the Widget Owner.
                </li>
                <li className='tos-list-item'>
                    <font color="darkred">Limitation of Liability: </font>
                    The Widget Owner shall not be liable for any damages arising out of the use or inability to use the Widget, including but not limited to, damages for loss of profits, loss of data, or other intangible losses.
                </li>
                <li className='tos-list-item'>
                    <font color="darkred">Modifications to the Widget: </font>
                    The Widget Owner may modify or discontinue the Widget at any time without notice. The User agrees that the Widget Owner shall not be liable to the User or any third party for any modification, suspension, or discontinuance of the Widget.
                </li>
                <li className='tos-list-item'>
                    <font color="darkred">Intellectual Property: </font>
                    The Widget and all intellectual property rights therein are and shall remain the property of the Widget Owner. The User agrees not to copy, modify, or distribute the Widget or any portion thereof without the express written consent of the Widget Owner.
                </li>
                <li className='tos-list-item'>
                    <font color="darkred">Indemnification: </font>
                    The User agrees to indemnify and hold harmless the Widget Owner, its affiliates, and their respective directors, officers, employees, and agents from any and all claims, damages, liabilities, costs, and expenses, including reasonable attorneys' fees, arising out of the User's use of the Widget.
                </li>
                <li className='tos-list-item'>
                    <font color="darkred">Termination: </font>
                    This Agreement may be terminated by either party at any time for any reason. Upon termination, the User must immediately cease all use of the Widget.
                </li>
                <li className='tos-list-item'>
                    <font color="darkred">Governing Law: </font>
                    This Agreement shall be governed by and construed in accordance with the laws of the United States of America. Any dispute arising under or in connection with this Agreement shall be resolved accordingly.
                </li>
                <li className='tos-list-item'>
                    <font color="darkred">Entire Agreement: </font>
                    This Agreement constitutes the entire agreement between the parties and supersedes all prior or contemporaneous agreements or representations, whether written or oral, relating to the Widget.
                </li>
            </ol>
        <p>By using the Widget, the User acknowledges that they have read this Agreement, understand it, and agree to be bound by its terms and conditions.</p>
    </div>
}