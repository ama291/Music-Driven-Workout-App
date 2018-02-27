//
//  WorkSummaryViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class WorkSummaryViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {

    var userid: String!
    var themes: String!
    var categories: String!
    var musclegroup: String!
    var equipment: String!
    var duration: String!
    var difficulty: String!
    var token: String!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        requestWorkout()
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
    
    /* Make a call to getWorkout() */
    struct usernameResult: Codable {
        var Result: String
        var Status: String
    }
    
    @objc func getWorkout() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/workouts/getworkout") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + userid + "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(usernameResult.self, from: data) else { return }
                print(json)
                DispatchQueue.main.async {
                }
            }
            }.resume()
    }
    
    @objc func requestWorkout() {
        let apiRoute = "http://138.197.49.155:8000/api/workouts/getworkout/"
        guard let myUrl = URL(string: apiRoute) else {
            print("Failed to construct URL")
            return
        }
        
        let request = URLRequest(url: myUrl)
        var query = "userid=" + userid + "&key=SoftCon2018"
        query += "&themes" + themes
        query += "&categories" + categories
        query += "&musclegroups" + musclegroup
        query += "&equipment" + equipment
        query += "&duration" + duration
        query += "&difficulty" + difficulty
        query += "&token" + token
        print(query)
        
        let session  = URLSession.shared
        session.dataTask(with: request)
    }
    
    /* The Table View */
    let sections = ["Exercises"]
    let exercises = ["Test Input 1", "Test Input 2"]
    
    func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return sections[section]
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return sections.count
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        switch section {
        case 0:
            // Exercise Section
            return exercises.count
        default:
            return 0
        }
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        // Create an object of the dynamic cell "PlainCell"
        let cell = tableView.dequeueReusableCell(withIdentifier: "PlainCell", for: indexPath)
        // Depending on the section, fill the textLabel with the relevant text
        switch indexPath.section {
        case 0:
            // Exercise Section
            cell.textLabel?.text = exercises[indexPath.row]
            break
        default:
            break
        }
    
        // Return the configured cell
        return cell
    }

}
