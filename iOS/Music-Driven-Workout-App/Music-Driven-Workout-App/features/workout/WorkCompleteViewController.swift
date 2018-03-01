//
//  WorkCompleteViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class WorkCompleteViewController: UIViewController {
    
    var userid: String!
    var workoutjson: String!
    var workoutid: String!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        //TODO: quitWorkout api call
        //quitworkoutapi()
        
        //TODO: display workout same way as workout summary
        
        //TODO: button onclick save workout api call
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
    
    struct jsonRequest: Codable {
        var Result: String
        var Status: String
    }
    
    @objc func quitworkoutapi() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/quitworkout/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        //userid, workoutid, key
        let postString = "userid=" + userid + "&workoutid=" + workoutid +  "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                print(json)
            }
            
        }.resume()
    }
    
    @objc func saveworkoutapi() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/saveworkout/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        //userid, workoutid, key
        let postString = "userid=" + userid + "&workoutid=" + workoutid +  "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                print(json)
            }
            
        }.resume()
    }
}
