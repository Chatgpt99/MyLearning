import React from "react";

class AddContact extends React.Component {
    state = {
        name: "",
        email: ""
    };

    add = (e) => {
        e.preventDefault();
        console.log("e => ", e);
        if(this.state.name === "" || this.state.email === "")
        {
            alert("This field is required");
            return;
        }
        console.log("state => ", this.state);
        this.props.myAddContactHandler(this.state);
        this.setState({name: "", email: ""});
    }

    render() {
        return (
            <div className='ui name'>
                <hr></hr>
                <hr></hr>
                <h2>Add Contact</h2>
                <form className="ui form" onSubmit={this.add}>
                    <div className="field">
                        <label>Name</label>
                        <input
                            type="text"
                            name="name"
                            placeholder="Your name"
                            value={this.state.name}
                            onChange={(e) => this.setState({ name: e.target.value })}
                        >
                        </input>
                    </div>
                    <div className="field">
                        <label>Email</label>
                        <input
                            type="email"
                            name="email"
                            placeholder="Your email"
                            value={this.state.email}
                            onChange={(e) => this.setState({ email: e.target.value })}
                        >
                        </input>
                    </div>
                    <button className="ui button blue">Add</button>
                </form>

            </div>
        );
    }
}

// class AddContact extends React.Component {
//     state = {
//         name: "",
//         email: ""
//     }

//     add = (e) => {
//         e.preventDefault(); 
//         if(this.state.name === "" || this.state.email === "") {
//             alert("All the fields are mandatory!");
//             return;
//         }
//         this.props.myAddContactHandler(this.state);
//         console.log("state => ", this.state);
//         this.setState({name: "", email: ""});
//     }

//     render() {
//         return (
//             <div className="ui main">
//                 <h2>Add Contact</h2>
//                 <form className="ui form" onSubmit={this.add}>
//                     <div className="field">
//                         <label>Name</label>
//                         <input
//                             type="text"
//                             name="name"
//                             placeholder="Write Your Full Name"
//                             onChange={(e) => this.setState({name: e.target.value})}
//                             value={this.state.name}
//                         />
//                     </div>
//                     <div className="field">
//                         <label>Email</label>
//                         <input 
//                             type="text"
//                             name="email"
//                             placeholder="Write your email"
//                             onChange={(e) => this.setState({email: e.target.value})}
//                             value={this.state.email}
//                         />
//                     </div>
//                     <button className="ui button primary">Add</button>
//                 </form>
//             </div>
//         );
//     }
// }

export default AddContact;