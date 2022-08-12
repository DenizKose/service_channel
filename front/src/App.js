// Importing modules
import React, {useEffect, useState} from "react";
import {Col, Container, Image, Nav, Row, Table} from 'react-bootstrap'
import "./App.css";
import moment from 'moment'
import 'moment/locale/ru'
import {
	CartesianGrid,
	Line,
	LineChart,
	BarChart,
	ComposedChart,
	Tooltip,
	XAxis,
	YAxis,
	Bar,
	ResponsiveContainer, Legend
} from "recharts";


function App() {


	console.log(moment.locale('ru'))

	const [data, setData] = useState(null);
	const [data_total, setDataTotal] = useState(null);

	useEffect(() => {
		const interval = setInterval(() => {
			fetch("/data")
			.then((res) => res.json())
			.then((data) => {
				setData(data['results'])
			})
			.catch((error) => {
				console.log(error)
				console.log(moment(new Date()).format('MMMM Do YYYY, h:mm:ss a'))
			})
			.finally(() => {
			});

			fetch("/data/order_by_date_and_values")
			.then((res) => res.json())
			.then((data_total) => {
				setDataTotal(data_total['results'])
			})
			.catch((error) => {
				console.log(error)
				console.log(moment(new Date()).format('MMMM Do YYYY, h:mm:ss a'))
			})
			.finally(() => {
			});
		}, 1000);
		return () => clearInterval(interval)
	}, []);


		return (
		<div className="App">
			<Container fluid>
			<Row>
				<Nav className={"navbar navbar-light bg-light"}>
					<div className="container-fluid">
							<a className="navbar-brand" href="/">
								<Image src={'/logo192.png'} className={"w-25 d-inline-block align-text-center me-5"}/>
									Каналсервис
							</a>
					</div>
				</Nav>
			</Row>
			<Row>
				<Col>
					<ResponsiveContainer width={'90%'} height={400	}>
						<LineChart
							  data={data_total && data_total.sort((a,b) => new Date(a.date)-new Date(b.date))
								  .map(({total, date }) => ({'total':total, 'date':moment(date).format('L')}))}
							  margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
								<CartesianGrid stroke="#ccc" />
								<XAxis name='Date' dataKey="date" interval={7}/>
								<YAxis />
								<Tooltip />
								<Legend />
								<Line name='Total' type='monotone' dataKey="total" fill="#413ea0" />
						</LineChart>
					</ResponsiveContainer>
				</Col>
				<Col>
					<Table striped bordered hover>
					  <thead>
						<tr>
						  <th>№</th>
						  <th>Заказ №</th>
						  <th>Стоимость $</th>
						  <th>Стоимость</th>
						  <th>Срок поставки</th>
						</tr>
					  </thead>
					  <tbody>
						{ data &&
							  data.sort((a,b) => a.id-b.id).map(({ id, order_id, value_usd, value_rub, delivery_date }) => (
								<tr key={id}>
								  <td>{id}</td>
								  <td>{order_id}</td>
								  <td>{value_usd}</td>
								  <td>{value_rub}</td>
								  <td>{moment(delivery_date).format('L')}</td>
								</tr>
							  ))}
					  </tbody>
					</Table>
				</Col>
			</Row>
			<Row>
				<center><a href='https://github.com/DenizKose/channel_service'>Проект на GitHub</a></center>
			</Row>
			</Container>
		</div>
	);
}

export default App;
