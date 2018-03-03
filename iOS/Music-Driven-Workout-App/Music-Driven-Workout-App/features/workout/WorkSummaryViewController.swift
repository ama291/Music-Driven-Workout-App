//
//  WorkSummaryViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

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
    //var player: SPTAudioStreamingController?

    //spotify
    var auth = SPTAuth.defaultInstance()!
    var session:SPTSession!
    
    //variables to send to WorkExerciseVC
    var workoutjson: String!
    var exNames: [String] = []
    var exDesc: [String] = []
    var exDur: [Int] = []
    var exImgs: [String] = []
    var exTrackNames: [[String]] = [[]]
    var exTrackUris: [[String]] = [[]]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
        
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
            vc?.workoutjson = workoutjson
            vc?.exercisenames = exNames
            vc?.exercisedescriptions = exDesc
            vc?.exercisedurations = exDur
            vc?.exerciseimages = exImgs
            vc?.exercisetracknames = exTrackNames
            vc?.exercisetrackuris = exTrackUris
            //vc?.player = player!
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
        
        request.submitPostServer(route: route, qstring: query) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            
            let resultjson = try? JSONSerialization.jsonObject(with: data!, options: [])
            self.workoutjson = String(describing: data)
            print("resultJson: ", resultjson as Any, "\n")
            
            if let dictionary = resultjson as? [String: Any] {
                if let exercises = dictionary["Exercises"] as? [Any] {
                    var exIndex = 0
                    for ex in exercises {
                        if let exDict = ex as? [String: Any] {
                            // Populate tableContent
                            let content = exDict["name"] as! String
                            self.tableContent.append(content)
                            
                            // Populate data to send to next scene
                            self.exNames.append(exDict["name"] as! String)
                            self.exDesc.append("exDescription")
                            self.exDur.append((exDict["duration"] as! Int) * 60) // convert to secs
                            self.exImgs.append(exDict["images"] as! String)
                            
                            if let trackDict = exDict["tracks"] as? [Dictionary<String, String>] {
                                for track in trackDict {
                                    print("Track:", track)
                                    print("TName:", track["name"] as Any)
                                    print("TUri:", track["uri"] as Any)
                                    self.exTrackNames[exIndex].append(track["name"]!)
                                    self.exTrackUris[exIndex].append(track["uri"]!)
                                    
                                    // Populate Song List
                                    self.songList.append(track["name"]!)
                                }
                            }
                            print(self.exTrackNames)
                            print(self.exTrackUris)
                        }
                        exIndex += 1
                        self.exTrackNames.append([])
                        self.exTrackUris.append([])
                    }
                }
            }
            
            DispatchQueue.main.async {
                self.exTable.delegate = self
                self.exTable.dataSource = self
                self.exTable?.reloadData()
            }
            
        }.resume()
    }

    
    /* Mark: tableView */
    @IBOutlet weak var exTable: UITableView!
    let sections = ["Exercises", "Songs"]
    var tableContent: [String] = []  //populated by getWorkout()
    var songList: [String] = []  //populated by getWorkout()
    
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
        case 1:
            return songList.count
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
        case 1:
            cell.textLabel?.text = songList[indexPath.row]
            break
        default:
            break
        }

        // Return the configured cell
        return cell
    }
    
}
