//
//  CESelectionViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class CESelectionViewController: UIViewController {

    var category: String = ""
    var muscleGroup: String = ""
    var equipment: String = ""
    
    struct jsonResponse: Codable {
        var Result: String
        var Status: String
    }
    
    func parseJsonRespone(response: String) {
        
        var res: Dictionary<String, String>
        
        if let data = response.data(using: String.Encoding.utf8) {
            do {
                res = try JSONSerialization.jsonObject(with: data, options: []) as! Dictionary<String, String>
                let myDict = res
                print("name: ", myDict["Status"]!)
                if let result = myDict["Result"] {
                    var reply: Dictionary<String, Any>
                    
                    if let resultData = result.data(using: String.Encoding.utf8) {
                        do {
                            reply = try JSONSerialization.jsonObject(with: resultData, options: []) as! Dictionary<String, Any>
                            let myReplyDict = reply
                            print("reply: ", myReplyDict)
                        }
                    }
                    print("hi")
                }
                
            } catch let error as Error {
                print(error)
            }
        }
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
        
        let str = "{\"Status\":\"OK\", \"Result\": \"{}\"}"

        parseJsonRespone(response: str)

//
//
//        let qstr = "category=" + category + "&muscle=" + muscleGroup + "&equipment=" + equipment + "&key=SoftCon2018"
//
//        self.submitPostLocal(route: "/api/fitness/getexsbytype/", qstring: qstr) { (data, response, error) -> Void in
//            if let error = error {
//                fatalError(error.localizedDescription)
//            }
//            guard let json = try? JSONDecoder().decode(jsonResponse.self, from: data!) else { return }
//            print(json.Result)
//
////            let jsonData = json.Result.data(using: .utf8)
////            let decoder = JSONDecoder()
////            let arr = try! decoder.decode([String].self, from: jsonData!)
////            print(arr)
//            }.resume()


        // Do any additional setup after loading the view.
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
