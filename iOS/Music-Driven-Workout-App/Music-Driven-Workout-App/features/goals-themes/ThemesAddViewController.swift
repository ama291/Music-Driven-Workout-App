//
//  ThemesAddViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class ThemesAddViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    let request = APIRequest()
    var themeName: String! = "theme1"
    var theme: String! = "Artist"
    var spotifyId: String! = "example-id"
    var numWorkouts: Int = 5
    var reply: String?
    var themeDict: [String:Any] = [:]
    var userid: String! = "21"
    var tableArray: [String: Dictionary<String, Any>] = [:]
    var token = global.token!
    var listNames: [String] = []
    var artistURIs: [String] = []

    
    @IBOutlet weak var tableView: UITableView!
    
    @IBOutlet weak var numWorkoutsLabel: UILabel!
    @IBOutlet weak var themeNameTextField: UITextField!
    @IBOutlet weak var spotifySearchbar: UITextField!
    @IBOutlet weak var numLabel: UILabel!
    
    @IBAction func saveTheme(_ sender: Any) {
        let qstr = "userid=\(userid!)&name=\(themeName!)&spotifyId=\(spotifyId!)&theme=\(theme!)&numworkouts=\(numWorkouts)&key=SoftCon2018"
        self.request.submitPostLocal(route: "/api/themes/addtheme/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = self.request.parseJsonInitial(data: data!)
            if self.reply != "0" {
                print("Add theme request failed")
                return
            }
            }.resume()
    }
    @IBAction func numChanged(_ sender: UISlider) {
        self.numWorkouts = Int(sender.value)
        numLabel.text = "Number of Workouts: " + String(numWorkouts)
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if (self.tableArray["artists"] != nil) {
            let names = self.tableArray["artists"]!["items"] as? NSArray
            return(names!.count)
        }
        else { return 0 }
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "themescell", for: indexPath) as UITableViewCell
//        if(self.tableArray["artists"] != nil) {
//            let names = self.tableArray["artists"]!["items"] as? NSArray
//            if let item = names![indexPath.row] as? NSDictionary {
//                cell.textLabel?.text = item["name"]
//            }
//        }
        cell.textLabel?.text = listNames[indexPath.row]
        return cell
    }
    
    @IBOutlet weak var artistToSearchFor: UITextField!
    @IBAction func searchForTheme(_ sender: UIButton) {
        print("token")
        print(token)
        let artistToSearchFor2 = artistToSearchFor.text!.replacingOccurrences(of: " ", with: "%20", options: .literal, range: nil)
        let postString = "q=" + artistToSearchFor2 + "&type=artist&limit=5"
        guard let url = URL(string: "https://api.spotify.com/v1/search?" + postString) else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("Authorization: Bearer " + token, forHTTPHeaderField: "Authorization")
      
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            guard let content = data else {
                print("not returning data")
                return
            }
            guard let json = (try? JSONSerialization.jsonObject(with: content, options: JSONSerialization.ReadingOptions.mutableContainers)) else {
                print("Not containing JSON")
                return
            }
            if let array = json as? [String : Dictionary<String,Any>] {
                self.tableArray = array
            }
//            print("spotify result")
//            print(self.tableArray["artists"])
            print("tyring")
//            print(self.tableArray.count)
            if let names = self.tableArray["artists"]!["items"] as? NSArray {
                print(names.count)
                self.listNames = []
                self.artistURIs = []
                for item in names {
//                    print(item)
//                    print((item as AnyObject).count)
//                    print(type(of:item))
                    if let item2 = item as? [String: AnyObject] {
//                        print(item2["name"])
                        self.listNames.append(item2["name"] as! String)
                        self.artistURIs.append(item2["uri"] as! String)
                    }
                }
            }
//            for (name, artist) in self.tableArray["artists"]!{
//                if(name == "items") {
//                    for item in (self.tableArray["artists"]!["items"]) {
//                        print(item)
//                    }
//                } else {
//                    continue
//                }
//            }
            DispatchQueue.main.async {
                print("table array")
                print(self.tableArray)
                self.tableView.reloadData()
            }
            }.resume()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        self.numWorkoutsLabel.text = "Number of Workouts: \(numWorkouts)"
        self.tableView.register(UITableViewCell.self, forCellReuseIdentifier: "themescell")
        self.tableView.dataSource = self
        self.tableView.delegate = self
        // Do any additional setup after loading the view.
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is ThemesMenuViewController
        {
            let vc = segue.destination as? ThemesMenuViewController
            vc?.userid = userid
            self.themeDict = ["name": self.themeName, "theme": self.theme, "numWorkouts": self.numWorkouts]
            print(themeDict)
            vc?.themes.append(self.themeDict)
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    /* Navigation */
    @IBAction func goBackToThemesMenu(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "goals-themes", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "themesID") as! ThemesMenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }

    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        
        // update ViewModel item
        let artists = tableArray["artists"]!["items"]! as! [[String:Any]]
        print(artists.count)
        print(indexPath.row)
        let artist = artists[indexPath.row]
        self.themeName = artist["name"]! as! String
        self.theme = "artist"
        self.spotifyId = artist["id"] as! String
        print(self.theme)
        print(self.themeName)
    }
    
}
