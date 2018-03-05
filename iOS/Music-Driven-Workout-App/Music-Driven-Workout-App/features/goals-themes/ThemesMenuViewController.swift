//
//  GoalsMenuViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//
import UIKit

class ThemesMenuViewController: UIViewController, UITableViewDelegate, UITableViewDataSource{
    
    var tableArray = [String:Any] ()
    var token: String!
    var passedUserId = String()
    
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.tableView.dataSource = self
        self.tableView.delegate = self
        // Do any additional setup after loading the view.
        populateThemes()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    /* Navigation */
    
    struct themesResult: Codable {
        var Result: String
        var Status: String
    }
    
    func populateThemes() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/workouts/themessaved/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "userid=" + global.userid + "&key=SoftCon2018"
        passedUserId = global.userid
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            guard let content = data else {
                print("not returning data")
                return
            }
            guard let json = (try? JSONSerialization.jsonObject(with: content, options: JSONSerialization.ReadingOptions.mutableContainers)) as? [String: Any] else {
                print("Not containing JSON")
                return
            }
            
            if let array = json as? [String: Any] {
                self.tableArray = array
                print(self.tableArray)
            }
            
            print(self.tableArray)
            DispatchQueue.main.async {
                self.tableView.reloadData()
            }
            }.resume()
    }
    
    
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        present(vc, animated: true, completion: nil)
    }
    
    @IBAction func goToAddTheme(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "themesAdd") as! ThemesAddViewController
<<<<<<< HEAD
        vc.userid = userid!
        vc.token = token!
=======
>>>>>>> 86dfa0c7934476390bfb7bc4b7f80bb69888be35
        present(vc, animated: true, completion: nil)
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath) as UITableViewCell
        cell.textLabel?.text = (self.tableArray["Result"]! as! String)
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.tableArray.count/2
    }
    
}
