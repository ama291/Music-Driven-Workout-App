# Sending Data Through A Segue
```
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is MenuViewController
        {
            let vc = segue.destination as? MenuViewController
            //data to send
            vc?.userid = userBox.text!
        }
    }
    
    @IBAction func goButtonClick(_ sender: Any) {
        self.performSegue(withIdentifier: "loginSegue", sender: self)
    }
```

# Making a HTTP Request And Updating A UI Element
```
    //json response struct - need to change this to what you expect the result to be
    struct jsonRequest: Codable {
        var Result: String
        var Status: String
    }
    
    @objc func postRequest() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/getusername/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + userid + "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                print(json)
                DispatchQueue.main.async {
                    //ui updates here
                    self.titletext.text = "Welcome back, " + json.Result + "!"
                }
            }
            
        }.resume()
    }
```
