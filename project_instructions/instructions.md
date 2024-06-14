# Software/Data Engineer Exercise
This assignment is intended to provide you a taste of what we are building here at Silk and allow you to experiment with some of the concepts you will encounter in your day to day job. We hope you **enjoy** ❤️.

## Assignment
Within Silk we have built a complex data pipeline. In this exercise we will implement 3 of the most important steps of such a pipeline:
1. Data Fetching - You will implement API clients to fetch raw hosts from a third party vendor (Qualys / Crowdstrike).
2. Data Normalization - You will implement logic to normalize the hosts (which are in different formats) into a unified format (that you'll define)
3. Data Deduping - You will implement logic to determine and merge duplicate hosts

> Note \
> 👉 Please use **Python 3.10** 🐍 and **MongoDB**

We created [mockup APIs for Qualys and Crowdstrike ](https://api.recruiting.app.silk.security/docs). Both tools, run local agents on hosts, and scan them periodically. The apis we implemented provide you access to the scanned hosts. You can find your API token in the [profile](https://recruiting.app.silk.security/profile) page.

## Instructions & Tips
1. Build a data pipeline as described above.
2. Ensure the code works and provide a simple readme (~10 lines) to run locally
3. Ensure code quality is of high standards 
   1. Use proper typing
   2. Split your code into files / logical components - don't submit a single file 
4. Think about how you would scale this system to support ~Millions of objects
5. Add **meaningful** visualization of the deduped/merged hosts (post screenshots 📷 in the github page). Examples:
   1. Distribution of host by operating system 
   2. Old hosts (last seen more than 30 days ago) vs newly discovered hosts 

## Submission
In order to submit your exercise, please share your PRIVATE github link below.
Remember to invite b@--- and w@--- to the repository.

(https://recruiting.app.silk.security/core)