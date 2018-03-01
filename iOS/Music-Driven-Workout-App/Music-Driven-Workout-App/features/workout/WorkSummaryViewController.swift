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
    
    /* Mark: Make a call to getWorkout() */
    var reply: [String:Any] = [String:Any]()
    var exerciseInfo: [String:Any] = [String:Any]()
    var exList: [String] = [String]()
    
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
        print("\nQUERY:" + query + "\n")

        request.submitPostLocal(route: route, qstring: query) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = request.parseWorkoutJson(data: data!)!   // ERR: data = nil so it can't be unwrapped
            
            print(self.reply)
            
            for rep in self.reply {
                //self.exList.append(rep["name"]! as! String)
                print(self.exList)
            }
            DispatchQueue.main.async {
            }
            
        }.resume()
    }
    
    /* Mark: tableView */
    let sections = ["Exercises"]
    //let exList = ["Test Input 1", "Test Input 2"]
    
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
            // Exercise Section
            return exList.count
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
            cell.textLabel?.text = exList[indexPath.row]
            break
        default:
            break
        }
    
        // Return the configured cell
        return cell
    }

}
