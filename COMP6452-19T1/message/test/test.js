const assert = require('assert');
const ganache = require('ganache-cli');
const Web3 = require('web3');
const web3 = new Web3(ganache.provider());
const { interface, bytecode } = require('../compile');

let accounts;
let message;


beforeEach(async ()=>{
	//get account
	
	//web3.eth.getAccounts()
		
		accounts = await web3.eth.getAccounts();
		
	//.then(fetchedAccounts => {
		//console.log(fetchedAccounts);
		message = await new web3.eth.Contract(JSON.parse(interface))
			.deploy({data:bytecode, arguments:['Hi there!']})
			.send({from: accounts[0], gas:'1000000'})
	});

describe('Message',()=>{
	it('deploys a contract',() => {
		//console.log(message);
		assert.ok(message.options.address);
	});
	
	it('has a default message', async () =>{
		const initialmessage = await message.methods.message().call();
		console.log("default message:", initialmessage);
		assert.equal(initialmessage, 'Hi there!');
	})
	
	it('can change message', async () =>{
		await message.methods.setMessage('bye').send({from: accounts[0]})
		const newmessage = await message.methods.message().call();
		console.log("new message:",newmessage);
		assert.equal(newmessage, 'bye');
		
	})
	
});