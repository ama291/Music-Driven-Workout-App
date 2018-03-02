//
//  WorkSummaryViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

/* struct for holding JSON Response from API */
struct jsonRequest: Codable {
    var Result: String
    var Status: String
}

class WorkSummaryViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, SPTAudioStreamingPlaybackDelegate, SPTAudioStreamingDelegate {

    var userid: String!
    var themes: String!
    var categories: String!
    var musclegroup: String!
    var equipment: String!
    var duration: String!
    var difficulty: String!
    var token: String!
    var username: String!

    //spotify
    var auth = SPTAuth.defaultInstance()!
    var session:SPTSession!
    var player: SPTAudioStreamingController?

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        print("WorkSummaryVC")
        print("\t userid:" + userid)
        print("\t themes:" + themes)
        print("\t categories:" + categories)
        print("\t musclegroups:" + musclegroup)
        print("\t equipment:" + equipment)
        print("\t duration:" + duration)
        print("\t difficulty:" + difficulty)
        print("\t token:" + token + "\n")

        getWorkout()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


    /* Mark: Navigation */
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is WorkSelectionViewController {
            let vc = segue.destination as? WorkSelectionViewController
            vc?.userid = userid!
        }
        else if segue.destination is WorkExerciseViewController {
            let vc = segue.destination as? WorkExerciseViewController
            vc?.userid = userid!
        }
    }

    /* Mark: Make a call to getWorkout() API and Parse Result */
    @objc func getWorkout() {
        let request = APIRequest()
        let route = "/api/workouts/getworkout/"
        var query = "userid=" + userid + "&key=SoftCon2018"
        if musclegroup.isEmpty {
            query += "&categories=" + categories
        } else {
            query += "&musclegroups=" + musclegroup
        }
        query += "&equipment=" + equipment
        query += "&duration=" + duration
        query += "&difficulty=" + difficulty
        query += "&token=" + token

        request.submitPostLocal(route: route, qstring: query) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            /* Parse the returned json */
            guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data!) else { return }
            let resultData = json.Result.data(using: .utf8)
            let resultJson = try? JSONSerialization.jsonObject(with: resultData!, options: [])
            
            if let dictionary = resultJson as? [String: Any] {
                if let exercises = dictionary["Exercises"] as? [Any] {
                    for ex in exercises {
                        if let exDict = ex as? [String: Any] {
                            print(exDict["name"] as! String)  // debugging
                            // Add Exercise names to TableView
                            var content = exDict["name"] as! String
                            content += "\t Category: " + (exDict["category"] as! String)
                            content += "\t Muscle Group: " + (exDict["muscleGroup"] as! String)
                            print(content)
                            self.tableContent.append(content)
                        }
                    }
                }
            }
        }.resume()
    }

    /* Mark: tableView */
    let sections = ["Exercises"]
    var tableContent: [String] = [String]()  //populated by getWorkout()
    
    // Section Headers
    func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return sections[section]
    }
    // Number of sections in tableView
    func numberOfSections(in tableView: UITableView) -> Int {
        return sections.count
    }
    // Number of rows in each section of tableView
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        switch section {
        case 0:
            return tableContent.count
        default:
            return 0
        }
    }
    // Data to fill the tableView with
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        // Create an object of the dynamic cell "PlainCell"
        let cell = tableView.dequeueReusableCell(withIdentifier: "PlainCell", for: indexPath)

        // Depending on the section, fill the textLabel with the relevant text
        switch indexPath.section {
        case 0:
            cell.textLabel?.text = tableContent[indexPath.row]
            break
        default:
            break
        }

        // Return the configured cell
        return cell
    }
    

}

/* Old Code that went inside  request.submitPostLocal(){}.resume */
//var reply: [String:Any] = [String:Any]()
//var exerciseInfo: [String:Any] = [String:Any]()
//            /* Parse the json object returned by submitPostLocal() */
//            let json = try? JSONSerialization.jsonObject(with: data!, options: [])
//            print("JSON:", json as Any, "\n\n")
//            if let dictionary = json as? [String: Any] {
//                /* Parse Status */
//                if let status = dictionary["Status"] as? String {
//                    print("Status:", status)
//                }
//
//                /* Parse Result */
//                let result = dictionary["Result"] as! String
//                print("result: ", result)
//
//                if let resultData = result.data(using: .utf8, allowLossyConversion: false) {
//                    do {
//                        let reply = try JSONSerialization.jsonObject(with: resultData, options: []) as! [String: AnyObject]
//                        print("reply JSON:", reply as Any)
//                    } catch let error as NSError {
//                        print("Failed to Load: \(error.localizedDescription)")
//                    }
//                }
//
//            }
