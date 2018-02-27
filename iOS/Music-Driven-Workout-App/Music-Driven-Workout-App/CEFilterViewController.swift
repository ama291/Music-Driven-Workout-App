//
//  CEFilterViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class CEFilterViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {

    @IBOutlet weak var catPicker: UIPickerView!
    @IBOutlet weak var musclePicker: UIPickerView!
    @IBOutlet weak var equipPicker: UIPickerView!
   
    struct jsonResponse: Codable {
        var Result: String
        var Status: String
    }
    var data: [String] = [String]()
    
    func submitPostLocal(route: String, qstring: String, completion: @escaping (Data?, URLResponse?,Error?) -> Void) -> URLSessionDataTask {
        var urlComponents = URLComponents()
        urlComponents.scheme = "http"
        urlComponents.host = "127.0.0.1"
        urlComponents.port = 5000
        urlComponents.path = route
        urlComponents.query = "key=SoftCon2018"
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
        
        //json response struct - need to change this to what you expect the result to be
        struct Post: Codable {
            let key: String
        }
        

        
        submitPostLocal(route: "/api/fitness/getcategories/", qstring: "key=SoftCon2018"){ (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            guard let json = try? JSONDecoder().decode(jsonResponse.self, from: data!) else { return }
            print(json.Result)
        }.resume()

        
        self.catPicker.delegate = self
        self.catPicker.dataSource = self
        data = ["Strength", "Cardio"]
        // Do any additional setup after loading the view.
    }

    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return data.count
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return data[row]
    }
    
//    func pickerView(pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
//        updateLabel()
//    }
    
    @IBAction func getExercises(_ sender: Any) {
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
