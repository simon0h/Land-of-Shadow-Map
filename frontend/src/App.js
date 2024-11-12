import React, { useState } from "react";
import PathForm from './PathForm';

import "./App.css";

function App() {
	const [sourceSites, setSourceSites] = useState('');
	const [selectedSource, setSelectedSource] = useState(null);
  	const [selectedDestination, setSelectedDestination] = useState(null);
	const [sourceChanged, setsourceChanged] = useState(false);
	const [destinationChanged, setDestinationChanged] = useState(null);
	const [destAndSourceSel, setDestAndSourceSel] = useState(false);
	const [path, setPath] = useState([]);

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

	React.useEffect(() => {
		if (sourceChanged && destinationChanged) {
			setsourceChanged(false);
			setDestinationChanged(false);
			setDestAndSourceSel(false);
			const fetchPromise = fetch(`http://127.0.0.1:5000/getpath?source=${selectedSource}&destination=${selectedDestination}`);
			const responsePromise = fetchPromise.then(response => response.json())
			responsePromise.then(data => {
				console.log(data)
				if (data.pathExists) {
					setPath(data.pathName)
				}
				else {
					setPath(["No path available from " + selectedSource + " to " + selectedDestination])
				}
			})
			.catch(error => {
				console.error('Path request failed:', error);
			});
		}
	}, [destAndSourceSel]); 

	const handleSourceSelect = (key) => {
		setSelectedSource(key);
		setsourceChanged(true);
	};
	
	const handleDestinationSelect = (key) => {
		setSelectedDestination(key);
		setDestinationChanged(true);
	};

	const getPath = (e) => {
		e.preventDefault();
		console.log('Selected source:', selectedSource);
    	console.log('Selected destination:', selectedDestination);
		if (sourceChanged && destinationChanged) {
			setDestAndSourceSel(true);
		}
	}

  	return (
		<div className = "App">
			<form onSubmit = {getPath}>
				<div className = "container">
					<ul className = "pathList" id = "pathList">
						{path.map((item, i) => (
							<div key={i}>
								<li>{item}</li>
							</div>
						))}
					</ul>
				</div>
				<div className = "container">
					<ul className = "list" id = "sourceList">
						<h1>Source</h1>
						{Object.entries(sourceSites).map(([key, value]) => (
						<div key={key}>
							<li><button type = "button" className = "sourceButton" value = {key} onClick={() => handleSourceSelect(key)}>{key}</button></li>
						</div> ))}
					</ul>
					<ul className = "list" id = "destinationList">
						<h1>Destination</h1>
						{Object.entries(sourceSites).map(([key, value]) => (
						<div key = {key}>
							<li><button type = "button" className = "sourceButton" value = {key} onClick={() => handleDestinationSelect(key)}>{key}</button></li>
						</div> ))}
					</ul>
				</div>
				<button type = "submit" id = "submitButton">Submit</button>
			</form>
		</div>
  	);
}

export default App;
