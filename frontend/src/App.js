import React, { useState } from "react";
import PathForm from './PathForm';

function App() {
	const [sourceSites, setSourceSites] = React.useState('');

	React.useEffect(() => {
		const fetchPromise = fetch('http://127.0.0.1:5000/getmapdata');
		// fetch() returns a variable of type Promise
		// Promise is used to handle asynch operations
		// i.e. when we make the API call, it might take some time
		// So instead of waiting for the API call to finish and then running the rest of the code, 
		// a Promise is returned and rest of the code run.
		// When the API call is completed, the Promise variable (fetchPromise in this case) is assigned a value (this process is also called "resolving a promise") 
		// and the code continues.
		const responsePromise = fetchPromise.then(function(response) {
			return response.json();
		})
		responsePromise.then(function(data) {
			//console.log(data)
			setSourceSites(data);
		})
		.catch(function(error) {
			console.error('Request failed:', error);
		});
	}, []);

  	return (
		<div className="App">
			<div>
				{Object.entries(sourceSites).map(([key, value]) => (
					<div key={key}>
						{key}
					</div> ))}
			</div>
		</div>
  	);
}

export default App;
