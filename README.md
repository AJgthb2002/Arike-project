# Arike

### Screenshots
<table>
  <tr>
<td><img width="860" alt="image" src="https://user-images.githubusercontent.com/73184612/157190888-6e9cf795-a06a-4b7b-845e-b9377cda115f.png"> </td>
    <td><img width="947" alt="image" src="https://user-images.githubusercontent.com/73184612/157191164-38f94d0a-b196-4bb6-960e-8bae8641b0d1.png"></td>
  </tr>
  <tr>
   <td> <img width="949" alt="image" src="https://user-images.githubusercontent.com/73184612/157191459-a002f187-4939-4a24-bbb9-42793e89a05b.png"> </td>
    <td> <img width="950" alt="image" src="https://user-images.githubusercontent.com/73184612/157191962-746938bf-cd31-48cb-a92e-4d8ac741cf8c.png"> </td>
  </tr>
  <tr>
   <td> <img width="949" alt="image" src="https://user-images.githubusercontent.com/73184612/157192503-fa91a5f3-1ec0-4402-8585-d152fb8f32ef.png"> </td>
     <td> <img width="944" alt="image" src="https://user-images.githubusercontent.com/73184612/157191608-bf1feb37-15af-4342-944d-57b83bbb9027.png"> </td>   
  </tr>
  <tr>
    <td> <img width="872" alt="image" src="https://user-images.githubusercontent.com/73184612/157192226-ae7dfdc5-a551-4bed-bf25-e4f2f239417e.png"> </td>
     <td> <img width="911" alt="image" src="https://user-images.githubusercontent.com/73184612/157191822-01ab58ea-4a9f-4da0-80e3-dba2193f625e.png"> </td>
  </tr>
  </table>

<br/>

"Arike" is a Malayalam word that roughly translates to "Alongside" or "Besides" in English. 
The project caters to a system of specialized medical staff tending to patients under palliative care. 🩺

Generally, in palliative care, there are “Primary Health Centers” (PHC) and “Community Health Centers”(CHC). Each of these resides in a ward that belongs to one of the many LSGs (Local Self-Government) in a district. In every PHC, there are primary nurses whose job is to visit patients locality-wise every month, go through their case sheets, and provide them with the care they need. If a particular patient needs expert care, they are referred to a specialist nurse who comes from the CHC.

***
### 🧑‍🤝‍🧑 The main users for Arike are:

- 👩‍⚕️ **Primary Nurse**: This user persona is responsible for maintaining all the health records for a particular patient under their PHC. <br/><br/>
Here is how they will interact with the system:<br/><br/>
**Manage list of patients**: Filtering and sorting the patients should be doable. <br/><br/>
**CRUD operations on patient object**: A nurse can register a patient with their personal details to the facility the former belongs to and update the below categories during the first visit.<br/><br/>
A patient object has 4 major categories: 1. Personal Details, 2. Family Details, 3. Health Information, 4. Treatment history <br/><br/>
**Visit the patient**: During a visit, a primary nurse will be adding health information, viewing the active treatments, and adding notes for each active treatment in that particular visit. The nurse will also be able to refer the patient to any secondary nurse in the district, especially based on their skill set (treatments they specialize in) from the patient dashboard. They can always view the patient dashboard and make edits to the first 2 categories above.<br/><br/>
**Schedule a visit**: A nurse will be able to prioritize their visits to critical patients on a daily basis. They should have a daily agenda view like in any digital calendar which they can reschedule and cross off their visits as they go about their day.<br/><br/>
***
- 👨‍⚕️ **Secondary Nurse**: This user persona belongs only to a CHC and is the specialist nurse that provides special care for a patient when referred by a primary nurse. <br/>
They have equal access to all data and interact with the system exactly like a primary nurse. The only difference is that they deal with patients being referred to them. They can see all data, including all the patient objects under their CHC.

***
- 👨‍💼 **District Admin**: <br />
This user persona has access to records under the user’s district. This user has full access to the data and should be able to create and delete Primary or Secondary nurses. <br/><br/>
Here is how they will interact with the system: <br/> <br/>
**Manage facilities**: Admin will maintain a list of facilities and all their relevant data. Every facility belongs to a ward but not every ward has a facility. Every patient also belongs to a ward, but can be registered in any facility. Filtering and sorting should also be doable.<br/><br/>
**Registering and managing nurses**: Since this system has to be secure and allow only verified nurses to access the critical health records of patients, the admin will be responsible for filling out forms with the details of the nurses to be onboarded. <br/><br/>
**Assign nurses to facilities**: Only the admin has the power to assign nurses (primary or secondary) to each facility. This can be done while registering. <br/>

***
#### Other entities:
- Facility: Can be a PHC or CHC.
- Patient: Patient is an object whose data we are dealing with, and they never get to use the software. A patient is registered in a PHC and is only referred to a CHC.
