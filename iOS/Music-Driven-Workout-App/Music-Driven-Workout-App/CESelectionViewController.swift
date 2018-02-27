//
//  CESelectionViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class CESelectionViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {

    @IBOutlet weak var exPicker: UIPickerView!
    
    var category: String = ""
    var muscleGroup: String = ""
    var equipment: String = ""
    
    var exList: [String] = [String]()
    
    func parseJsonRespone(data: Data) -> [Dictionary<String, Any>]? {
        var res: Dictionary<String, String>
        do {
            res = try JSONSerialization.jsonObject(with: data, options: []) as! Dictionary<String, String>
            let myDict = res
            if let result = myDict["Result"] {
                var reply: [Dictionary<String, Any>]
                
                if let resultData = result.data(using: String.Encoding.utf8) {
                    do {
                        reply = try JSONSerialization.jsonObject(with: resultData, options: []) as! [Dictionary<String, Any>]
                        let myReplyDict = reply
                        return myReplyDict
                    }
                }
            }
            
        } catch let error {
            print(error)
        }
        return nil
    }
    
  
    func submitPostLocal(route: String, qstring: String, completion: @escaping (Data?, URLResponse?,Error?) -> Void) -> URLSessionDataTask {
        var urlComponents = URLComponents()
        urlComponents.scheme = "http"
        urlComponents.host = "127.0.0.1"
        urlComponents.port = 5000
        urlComponents.path = route
        urlComponents.query = qstring
        guard let url = urlComponents.url else {
            fatalError("Could not create URL")
        }
        print(url)

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = qstring
        request.httpBody = postString.data(using: String.Encoding.utf8)
        print("jsonData: ", String(data: request.httpBody!, encoding: .utf8) ?? "no body data")

        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)
        let task = session.dataTask(with: request) {(data, response, responseError) in
            if let data = data {
                completion(data, response, responseError)
            }
        }
        return task
    }

    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        print("New view:", category, muscleGroup, equipment)
        
        let str = "{\"Status\":\"OK\", \"Result\": \"[{},{}]\"}"

        if let data = str.data(using: String.Encoding.utf8) {
            parseJsonRespone(data: data)
        }
//
        let qstr = "category=" + category + "&muscle=" + muscleGroup + "&equipment=" + equipment + "&key=SoftCon2018"

        self.submitPostLocal(route: "/api/fitness/getexsbytype/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            let reply = self.parseJsonRespone(data: data!)
            
//            names = reply.map { $0["name"] }
            print(reply![0]["name"]!)
            for rep in reply! {
                self.exList.append(rep["name"]! as! String)
            }
            DispatchQueue.main.async {
                self.exPicker.delegate = self
                self.exPicker.dataSource = self
            }

            
//            let jsonData = json.Result.data(using: .utf8)
//            let decoder = JSONDecoder()
//            let arr = try! decoder.decode([String].self, from: jsonData!)
//            print(arr)
            }.resume()


        // Do any additional setup after loading the view.
    }


    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return exList.count
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return exList[row]
    }
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
